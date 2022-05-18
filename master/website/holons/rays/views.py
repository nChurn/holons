import logging
import json
from functools import reduce

from django.conf import settings
from django.core import management
from django.http import HttpRequest, JsonResponse
from django.db.models import Q, CharField, TextField
from django.db.models.functions import Lower
from django.views.decorators.http import require_http_methods

from helpers.date_helper import pretty_date
from helpers import html_helper
from email_api.helpers import auth_helper
from email_api.helpers import request_helper
from accounts.models import User

from .models import CustomTalent
from .models.ray_source import RaySource
from .models.upwork_talent import UpworkTalent
from .models.talent import Talent



RAY_SOURCES = settings.RAY_SOURCES


'''
Plato's Flywheel functionality
'''
def search(request: HttpRequest) -> JsonResponse:
    """
    Search through Talents database

    :return: JsonResponse
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    talents_data = []
    search_string = data.get('search_string', None)
    geograpy_string = data.get('geo_string', None)
    # geograpy_string = get_geography(search_string)
    search_string = search_string.replace(geograpy_string, '')
    search_words = search_string\
        .replace('the ', '')\
        .replace(' a ', '')\
        .replace(' in ', '')\
        .replace(' on ', '')\
        .split(' ')
    CharField.register_lookup(Lower, "lower")
    TextField.register_lookup(Lower, "lower")
    if method == 'post':
        talents_raw = Talent.objects \
            .filter(
                Q(location__icontains=geograpy_string)
            )\
            .exclude(summary__isnull=True)\
            .filter(
                    Q(title__icontains=search_string)
                    | reduce(lambda x, y: x | y,
                      [Q(title__icontains=word) for word in search_words])
                    | reduce(lambda x, y: x | y,
                      [Q(summary__icontains=word) for word in search_words])
            )\
            .all()

        for talent in talents_raw[0:20]:
            talents_data.extend([{
                'name': talent.name,
                'company_name': talent.company_name,
                'summary': talent.summary,
                'location': talent.location
            }])

    if method == 'get':
        return JsonResponse({
            'result': 'Wrong method',
            'method': method,
        })

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'talents': talents_data
    })


def user_rays(request: HttpRequest) -> JsonResponse:
    """
    List Holons users' rays on GET
    Create new ray on POST

    :return: JsonResponse
    """

    user = request.user
    method = request.method
    rays_data = ''
    fixed_rays = []
    if method == 'POST':
        rays_data = create_new_ray(user, request)
    if method == 'GET':
        rays_data = list_user_rays(user)

        # that's a hack to make local development faster,
        # limit 20mb JSONs to 100 items 
        hostname = request.get_host()[:9]
        if 'localhost' == hostname:
            rays_data = rays_data[0:100]

        for fixed_ray in RAY_SOURCES:
            fixed_rays.extend(
                [{
                    fixed_ray: list(CustomTalent.objects.filter(
                      ray_source=RAY_SOURCES.index(fixed_ray)).all().values()
                    )
                }]
            )

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'rays': rays_data,
        'bids': {
            'total': user.platos_bids,
            'this_week': user.platos_bids_this_week,
        },
        # 'fixed_rays': fixed_rays
    })


def user_rays_status(request: HttpRequest) -> JsonResponse:
    """
    List Holons users' rays stats on GET

    :return: JsonResponse
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    if not user.id:
      return JsonResponse({
        'result': 'Error',
        'message': 'Access denied',
        'rays_count': '1'
      }, status=200)
      # }, status=403)
    if method != 'get':
      return JsonResponse({
        'result': 'Error',
        'message': 'Method not allowed'
      }, status=405)
    if method == 'get':
      rays_count = '5'

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'rays_count': rays_count,
    })


def create_new_ray(user: str, request: HttpRequest) -> str:
    """
    Create new RaySettings object and link it to the given User

    :param user:
    :param request:
    :return:
    """

    data = json.loads(request.body)
    ray = data.get('ray', None)
    title = ray.get('title', None)
    if title == '':
        title = 'Nameless ray'
    url = ray.get('source_url', None)
    stop_words = ray.get('exclude_countries', '')
    key_words = ray.get('key_words', '')
    is_active = ray.get('is_active', False)
    ray_settings = RaySource.objects.create()

    ray_settings.title = ray.get('title')
    ray_settings.link = ray.get('link')
    ray_settings.stop_words = stop_words
    ray_settings.key_words = key_words
    ray_settings.is_active = ray.get('is_active')
    ray_settings.title_filter = ray.get('title_filter')
    ray_settings.skills_filter = ray.get('skills_filter')
    ray_settings.category_filter = ray.get('category_filter')
    ray_settings.is_budget_empty_ok = ray.get('budget_empty')
    ray_settings.budget_rate = ray.get('budget_rate')
    ray_settings.budget_fixed = ray.get('budget_fixed')
    ray_settings.save()

    ray_settings.users.add(user)
    save_ray_settings(request, ray_settings.id)
    # @todo how cool is it?
    # Not sure if we should have settings logic separated in such a way
    logging.info('Ray settings attached to the user')
    logging.info('Call refresh rays command')
    # management.call_command('import_rays_rss')

    return 'New ray created'


def save_ray_settings(request: HttpRequest, pk: int) -> JsonResponse:
    """
    Get RaySettings object
    Update ray settings
    Store RaySettings in the database

    :param pk:
    :param request:
    :return:
    """

    method = request.method

    if method == 'GET':
        result = 'Get not allowed'

    ray_settings = RaySource.objects.filter(pk__exact=pk).first()

    if method == 'POST':
        data = json.loads(request.body)
        ray = data.get('ray', None)
        ray_settings.title = ray.get('title')
        ray_settings.link =  ray.get('link')
        ray_settings.stop_words = ray.get('stop_words')
        ray_settings.key_words = ray.get('key_words')
        ray_settings.is_active = ray.get('is_active')
        ray_settings.title_filter = ray.get('title_filter')
        ray_settings.skills_filter = ray.get('skills_filter')
        ray_settings.category_filter = ray.get('category_filter')
        ray_settings.is_budget_empty_ok = ray.get('budget_empty')
        ray_settings.budget_rate = ray.get('budget_rate')
        ray_settings.budget_fixed = ray.get('budget_fixed')
        ray_settings.save()
        result = 'Ray saved'

    if method == 'DELETE':
        ray_settings.delete()
        result = 'Ray deleted'

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'message': result
    })


def list_user_rays(user):
    """
    Get all user's RaySettings and send them as a list

    :param user:
    :return:
    """

    current_user_rays = user.rays.order_by('title').all()
    rays = []
    ray_to_extract = []
    for ray_setting in current_user_rays:
        messages = []
        deleted_count = 0
        archived_count = 0

        for message in ray_setting.messages.filter(is_deleted=True)\
            .all().exclude(is_expired=True)[0:1]:
            messages.extend([{
                'id': message.id,
                'title': message.title.replace(' - Upwork', ''),
                'description': message.description.replace(
                  '>click to ', ' style="display: none">click to '
                ),
                'url': message.link,
                'pub_date': message.pub_date,
                'deleted': message.is_deleted,
                'archived': message.is_archived,
                'proposed': message.is_proposed,
                'country': message.country,
            }])
            deleted_count += 1

        for message in ray_setting.messages.filter(is_archived=True)\
            .all().exclude(is_expired=True)[0:1]:
            messages.extend([{
                'id': message.id,
                'title': message.title.replace(' - Upwork', ''),
                'description': message.description.replace(
                  '>click to ', ' style="display: none">click to '
                ),
                'url': message.link,
                'pub_date': message.pub_date,
                'deleted': message.is_deleted,
                'archived': message.is_archived,
                'proposed': message.is_proposed,
                'country': message.country,
            }])
            archived_count += 1

        total_messages = ray_setting.messages.filter(is_deleted=False)\
            .order_by('-pub_date')\
            .filter(is_archived=False).all()\
            .exclude(is_expired=True)[0:10000]

        total_count = len(total_messages)

        for message in total_messages:
            # This is where we show trace message to certain people
            trace_message = ''
            if user.phone_number == settings.CTO_PHONE:
                trace_message = '<div class="trace_message hidden"><br /><strong>Trace</strong><br />'
                trace_message += message.trace_message.replace('\n', '<br />') + '<br /><br />'
                trace_message += '</div>'
            if False and user.phone_number == settings.CEO_PHONE:
                trace_message = '<div class="trace_message hidden"><br /><strong>Trace</strong><br />'
                trace_message += message.trace_message.replace('\n', '<br />') + '<br /><br />'
                trace_message += '</div>'
            budget = ''
            rate_from = ''
            rate_to = ''
            if message.budget is not None:
              budget = str(int(message.budget.amount))
            if message.rate_from is not None:
              rate_from = str(int(message.rate_from.amount))
            if message.rate_to is not None:
              rate_to = str(int(message.rate_to.amount))
            messages.extend([{
                'id': message.id,
                'title': message.title.replace(' - Upwork', ''),
                'description': trace_message + html_helper.sanitize_talent_description(message.description)
                    .replace('>click to ', ' style="display: none">click to ')
                    .replace(
                      'UTC<br />', 'UTC (' + pretty_date(message.pub_date) + ')<br />'
                    )                    ,
                'url': message.link,
                'pub_date': message.pub_date,
                'pub_date_pretty': pretty_date(message.pub_date),
                'deleted': message.is_deleted,
                'archived': message.is_archived,
                'proposed': message.is_proposed,
                'country': message.country,
                'budget': budget,
                'rate_from': rate_from,
                'rate_to': rate_to,
            }])
        ray = [{
            'id': ray_setting.id,
            'short_name': ray_setting.title,
            'url': ray_setting.link, 
            'exclude_countries': ray_setting.stop_words,
            'key_words': ray_setting.key_words,
            'is_active': ray_setting.is_active,
            'title_filter': ray_setting.title_filter,
            'skills_filter': ray_setting.skills_filter,
            'category_filter': ray_setting.category_filter,
            'budget_empty': ray_setting.is_budget_empty_ok,
            'budget_rate': ray_setting.budget_rate,
            'budget_fixed': ray_setting.budget_fixed,
            'messages': messages,
            'deleted_count': deleted_count,
            'archived_count': archived_count,
            'total_count': total_count
        }]

        rays.extend(ray)

        if ray_setting.title == 'ALL':
            ray_to_extract = ray
    if ray_to_extract:
        rays.append(rays.pop(rays.index(ray_to_extract[0])))

    # return sorted(rays, key=lambda e: e['total_count'], reverse=True)
    return rays


def rays_message(request: HttpRequest, pk) -> JsonResponse:
    """
    √ Get UpworkTalent message by pk / return error if no such message
    √ Check access method (patch/delete)
    √ if method is patch, set Archived flag
    √ if method is delete, set Deleted flag

    √ Save message
    √ Return OK

    :param request:
    :param pk:
    :return:
    """

    try:
        message = UpworkTalent.objects.filter(pk=pk).get()
    except UpworkTalent.DoesNotExist:
        return JsonResponse(status=404, data={'error': 'Message does not exist'})

    method = request_helper.method_name(request)
    if method == 'patch':
        message.is_archived = True
        message.is_proposed = True
    if method == 'delete':
        message.is_deleted = True

    message.save()

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'message': message.title
    })


def rays_users(request: HttpRequest) -> JsonResponse:
    """
    √ Return list of all users with access to Rays

    :param request:
    :return:
    """

    method = request_helper.method_name(request)
    if method == 'get':
        user_list = {}
        users = User.objects.all().values('id', 'username')
        for user in users:
            user_list[user['id']] = {'id': user['id'], 'username': user['username']}
        return JsonResponse({
            'result': 'OK',
            'method': method,
            'users': user_list
        })

    if method == 'post':
        user = auth_helper.get_user(request)
        logging.info(user.username)
        return JsonResponse({
            'result': 'OK',
            'method': method,
            'users_attached': 'attached',
            'owner_user': user.username
        })

