import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helpers.date_helper import pretty_date
from email_api.helpers import auth_helper
from email_api.helpers import request_helper
from accounts.models import User

from .models import CustomTalent
from .models.ray import Ray
from .models.message_thread import MessageThread
from .models.direct_message import DirectMessage


DEFAULT_RAY_MESSAGES = settings.DEFAULT_RAY_MESSAGES
RAY_SOURCES = settings.RAY_SOURCES
LOGIN_PARAMS = ('/auth', None)


@require_http_methods(["GET"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def user_rays_direct(request: HttpRequest) -> JsonResponse: 
    """
    List Holons users' Direct Rays on GET

    * take direct rays
    * take fixed rays and load messages in each of them

    :return: JsonResponse
    """

    rays_data = list_user_direct_rays(request.user)

    return JsonResponse({
        'result': 'OK',
        'rays': rays_data,
    })


def list_user_direct_rays(user: User) -> list:
    """
    Prepare a list of Ray->MessageThread->DirectMessage
    Enrich with from: and to: usernames

    """

    add_default_rays(user)
    user_direct_rays = []
    for ray in user.rays_direct.all():
      ray_message_threads = []
      messages_count = 0
      thread_count = 0
      user_from = ''
      user_to = ''
      for message_thread in ray.message_thread.all():
        messages = []
        note_to_self = False
        if not message_thread.is_archived and not message_thread.is_deleted:
          thread_count += 1
        if message_thread.messages:
          user_from = message_thread.messages.first().user_from.first()

        for message in message_thread.messages.all():
          sender_handle = ''
          sender_userpic = ''
          reciever_handle = ''
          reciever_userpic = ''
          if message.user_from.first():
            sender_handle = message.user_from.first().handle
            sender_account_status = message.user_from.first().account_status
            if sender_account_status == '':
              sender_account_status = settings.ACCOUNT_STATUSES[0][0]
            try:
              sender_userpic = message.user_from.first().userpic.url
            except ValueError:
              logging.info('Userpic does not exist')
          if message.user_to.first():
            reciever_handle = message.user_to.first().handle
            reciever_account_status = message.user_to.first().account_status
            if reciever_account_status == '':
              reciever_account_status = settings.ACCOUNT_STATUSES[0][0]
            try:
              reciever_userpic = message.user_to.first().userpic.url
            except ValueError:
              logging.info('Userpic does not exist')
          if message.user_to == message.user_from:
            note_to_self = True
          messages.extend([{
            'id': message.id,
            'subject': message.subject,
            'body': message.body,
            'pub_date': message.pub_date,
            'pub_date_pretty': pretty_date(message.pub_date),
            'is_archived': message.is_archived,
            'is_deleted': message.is_deleted,
            'provider': message.provider,
            'user_to': reciever_handle,
            'user_to_userpic': reciever_userpic,
            'user_to_account_status': reciever_account_status,
            'user_from': sender_handle,
            'user_from_userpic': sender_userpic,
            'user_from_account_status': sender_account_status,
          }])
        ray_message_threads.extend([{
          'id': message_thread.id,
          'is_archived': message.message_thread.is_archived,
          'is_deleted': message.message_thread.is_deleted,
          'messages': messages
        }])

      # :todo: investigate a correct way to get user_to
      user_to = ray.users.all().first()
      check_users = ray.users.all().exclude(pk=user_from.id)
      for el in check_users:
        user_to = el


      short_name = user_to.username.split(' ')[0] + ' @' + user_to.handle 
      if note_to_self:
        short_name = 'Notes to self'

      userpic = ''
      if user_to.userpic:
        userpic = user_to.userpic.url
      user_direct_rays.extend([{
        'id': ray.id,
        'short_name': short_name,
        'user_from_id': str(user_from.id),
        'user_to_id': str(user_to.id),
        'user_from': user_from.username,
        'user_to': user_to.username,
        'message_threads': ray_message_threads,
        'messages_count': thread_count,
        'userpic': userpic,
      }])

    return user_direct_rays
    

@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def rays_custom_message(request: HttpRequest) -> JsonResponse:
    """
    Send a custom message to the fixed ray
    * Moneta
    * Talant
    * etc

    :param request:
    :return:

    """

    if {} == json.loads(request.body):
      return JsonResponse({
          'result': 'error',
          'message': 'empty request'
      }, status=400)

    data = json.loads(request.body)
    title = data.get('title', None)
    description = data.get('description', None)
    ray_source_id = data.get('ray_source', None)
    # :todo: maybe we could unify errors?
    if not title:
      return JsonResponse({'result': 'error', 'message': 'empty title'}, status=400)
    if not description:
      return JsonResponse({'result': 'error', 'message': 'empty description'}, status=400)
    if not ray_source_id:
      return JsonResponse({'result': 'error', 'message': 'empty ray source'}, status=400)
    ray_source = RAY_SOURCES.index(ray_source_id)
    message = CustomTalent.objects.create(
        ray_source=ray_source,
        title=title,
        description=description
    )
    message.save()
    return JsonResponse({
        'result': 'OK',
        'message': message.title
    })


@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def rays_send_direct_message(request: HttpRequest) -> JsonResponse:
    """Send direct messages between two users via common Ray
    
    * get a common Ray for user_from and user_to
    * create new ray message in the common Ray

    """

    if {} == json.loads(request.body):
      return JsonResponse({
          'result': 'error',
          'message': 'empty request'
      }, status=400)

    data = json.loads(request.body)
    user_from = request.user
    to = data.get('to', None)

    if data.get('reply_to_id', False):
      user_to = get_message_author(data.get('reply_to_id'))
      message_sent = rays_add_thread_message(
        message_body=data.get('message_body', ''),
        reply_to_id=data.get('reply_to_id', None)
      )
      user_to.rays_dm_recieved.add(message_sent)
      user_from.rays_dm_sent.add(message_sent)
      return JsonResponse({
          'result': 'OK',
          'message': 'message sent as a reply',
      })
    elif not to:
      return JsonResponse({
                          'result': 'error',
                          'message': 'empty to'}, status=400)
    if not data.get('subject', None):
      return JsonResponse({
                          'result': 'error',
                          'message': 'empty subject'}, status=400)
    if not data.get('message_body', None):
      return JsonResponse({
                          'result': 'error',
                          'message': 'empty message_body'}, status=400)
    user_to = User.objects.filter(pk=to).get()
    subject = data.get('subject', '')
    message_body = data.get('message_body', '')
    direct_message = create_direct_message(user_from, user_to, subject, message_body)
    return JsonResponse({
        'result': 'OK',
        'message': 'message sent',
        'message_id': direct_message.id,
    })


def create_direct_message(user_from, user_to, subject, message_body) -> DirectMessage:
    """Prepare and save DirectMessage to the DB"""
    ''' Direct Ray '''
    common_ray = get_common_ray(user_from, user_to)
    ''' MessageThread '''
    message_thread = MessageThread.objects.create()
    common_ray.message_thread.add(message_thread)
    ''' DirectMessage '''
    direct_message = DirectMessage.objects.create(
      subject=subject,
      body=message_body,
      message_thread=message_thread,
    )
    user_from.rays_dm_sent.add(direct_message)
    user_to.rays_dm_recieved.add(direct_message)
    return direct_message


def get_common_ray(user_from: User, user_to: User) -> Ray:
    """Get common Ray between two users given

    * search for a Ray shared by the two users
    * create one if users have no Rays in common

    :param user_from:
    :param user_to:
    :returns: Common Ray ready for messaging
    """

    ''' In case the user has no direct rays at all '''
    if len(user_from.rays_direct.all()) == 0:
        common_ray = create_common_ray(user_from, user_to)
        return common_ray
    else:
      ''' Search for a common Ray '''
      for ray in user_from.rays_direct.all():
        for ray_user in ray.users.all():
          if user_to == ray_user:
            return ray
    common_ray = create_common_ray(user_from, user_to)
    return common_ray


def create_common_ray(user_from: User, user_to: User) -> Ray:
      """Create a common Ray for direct messaging between two users

      * create ray
      * attach users

      :param user_from:
      :param user_to:
      :returns: Common Ray ready for messaging
      """

      common_ray = Ray.objects.create()
      user_from.rays_direct.add(common_ray)
      user_to.rays_direct.add(common_ray)
      return common_ray



@require_http_methods(["DELETE"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def rays_thread_delete(request: HttpRequest, thread_id: int) -> JsonResponse:
    message_thread = MessageThread.objects.filter(pk=thread_id).get()
    message_thread.is_deleted = True
    message_thread.save()
    return JsonResponse({
        'result': 'OK',
    })


@require_http_methods(["PATCH"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def rays_thread_archive(request: HttpRequest, thread_id: int) -> JsonResponse:
    message_thread = MessageThread.objects.filter(pk=thread_id).get()
    message_thread.is_archived = True
    message_thread.save()
    return JsonResponse({
        'result': 'OK',
    })


def rays_add_thread_message(message_body: str, reply_to_id: int) -> DirectMessage:
    ''' DirectMessage '''
    parent_message = DirectMessage.objects.filter(pk=reply_to_id).get()
    message_thread = parent_message.message_thread
    direct_message = DirectMessage.objects.create(
      subject=parent_message.subject,
      body=message_body,
      message_thread=message_thread
    )
    return direct_message


def add_default_rays(user: User) -> bool:
    """Enhance user's direct_rays with default messages from RAY_SOURCES

    * get all user's DirectMessages
    * see if the result lacks message from any of the RAY_SOURCES
    * send message RAYSOURCE.name -> user.id

    :returns: True if any message sent, False if all default messages are there
    """

    fixed_users = get_fixed_users()
    fixed_users.insert(0, user.id)
    for f_id in fixed_users:
      rays_opened = user.rays_dm_recieved.all().filter(user_from__id=f_id).count()
      if 0 == rays_opened:
        if f_id == user.id:
          f_user = user
          subject = 'Note to self'
          message = 'Write something'
        else:
          f_user = User.objects.filter(pk__exact=f_id).get()
          subject = 'Greetings from: ' + f_user.username
          default_message = DEFAULT_RAY_MESSAGES[f_user.handle]
          message = default_message

        create_direct_message(
            user_from=f_user,
            user_to=user,
            subject=subject,
            message_body=message
          )


def get_fixed_users() -> list:
    """Get list of User ids based on a list of handles from SETTINGS"""

    fixed_users = User.objects.filter(handle__in=RAY_SOURCES)\
                  .values_list('id', flat=True)
    return list(fixed_users)


def get_message_author(message_id: int) -> User:
    message = DirectMessage.objects.filter(pk=message_id).get()
    return message.user_from.first()
