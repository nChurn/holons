import logging
import json

from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from accounts.models import User
from .models.ray_canned import RayCanned
from .direct_messages import create_direct_message
from .direct_messages import rays_add_thread_message


LOGIN_PARAMS = ('/auth', None)

@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def create(request: HttpRequest) -> JsonResponse:
    """Create a custom Rays template for automation purposes

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
    body = data.get('body', None)
    if not title:
      return JsonResponse({'result': 'error', 'message': 'empty title'}, status=400)
    if not body:
      return JsonResponse({'result': 'error', 'message': 'empty body'}, status=400)

    slug = title

    ray_canned = RayCanned.objects.create(
      title=title,
      slug=slug,
      body=body
    )

    request.user.rays_canned.add(ray_canned)

    return JsonResponse({
      'result': 'ok',
      'message': 'canned message created'
    })


@require_http_methods(["PATCH"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def update(request: HttpRequest) -> JsonResponse:
    """Update a custom Rays template for automation purposes

    :param request:
    :return:

    """

    if {} == json.loads(request.body):
      return JsonResponse({
          'result': 'error',
          'message': 'empty request'
      }, status=400)

    data = json.loads(request.body)
    item_id = data.get('id', None)
    title = data.get('title', None)
    body = data.get('body', None)
    if not item_id:
      return JsonResponse({'result': 'error', 'message': 'empty id'}, status=400)
    if not title:
      return JsonResponse({'result': 'error', 'message': 'empty title'}, status=400)
    if not body:
      return JsonResponse({'result': 'error', 'message': 'empty body'}, status=400)

    ray_canned = RayCanned.objects.filter(pk=item_id).first()
    ray_canned.title = title
    ray_canned.body = body
    ray_canned.save()

    return JsonResponse({
      'result': 'ok',
      'message': 'canned message saved'
    })


@require_http_methods(["DELETE"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def destroy(request: HttpRequest, item_id: int = None) -> JsonResponse:
    """Delete a custom Rays template for automation purposes

    :param request:
    :return:

    """
    
    if not item_id:
      return JsonResponse({'result': 'error', 'message': 'empty id'}, status=400)

    ray_canned = RayCanned.objects.filter(pk=item_id).first()
    ray_canned.delete()

    return JsonResponse({
      'result': 'ok',
      'message': 'canned message destroyed'
    })


@require_http_methods(["GET"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def list_all(request: HttpRequest) -> JsonResponse:
    """List custom Rays templates for automation purposes

    :param request:
    :return:

    """
    rays_canned = request.user.rays_canned.all()
    result = []
    for item in rays_canned:
      el = {
        'id': item.id,
        'title': item.title,
        'slug': item.slug,
        'body': item.body
      }
      result.append(el)
    return JsonResponse(result, safe=False)


@require_http_methods(["GET"])
def show(request: HttpRequest, slug: str) -> HttpResponse:
    """Show RaysCanned page

    :param request:
    :return:

    """

    canned_ray_message = RayCanned.objects.filter(slug=slug).first()
    canned_data = canned_ray_message
    return render(request, 'ray-canned.html', {
      'item': canned_data,
      'anonymous': request.user.is_anonymous
    })


@require_http_methods(["POST"])
def create_message(request: HttpRequest) -> JsonResponse:
    """Recieve POST, create a new Ray message, based on RayCanned settings
    and user provided data"""

    if {} == json.loads(request.body):
      return JsonResponse({
          'result': 'error',
          'message': 'empty request'
      }, status=400)

    data = json.loads(request.body)
    ray_id = data.get('id', None)
    message = data.get('message', None)
    if not ray_id:
      return JsonResponse({'result': 'error', 'message': 'empty id'}, status=400)
    if not message:
      return JsonResponse({'result': 'error', 'message': 'empty message body'}, status=400)
    # check if user is Anonymous
    if request.user.is_anonymous:
      user_from = User.objects.filter(email='anonymous.ray.sender@holons.me').first()
    else:
      user_from = request.user
    ray_canned = RayCanned.objects.filter(pk=ray_id).first()
    user_to = ray_canned.users.first()
    # initiate new Ray with a default message
    initial_message = create_direct_message(
        user_from=user_from,
        user_to=user_to,
        subject=ray_canned.title,
        message_body=ray_canned.body
      )
    # create a Ray message in reply to this newly created RayMessage
    message_sent = rays_add_thread_message(
      message_body=message,
      reply_to_id=initial_message.id
    )

    return JsonResponse({
      'result': 'ok',
      'message': 'message sent'
    })
