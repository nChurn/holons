import logging
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services import timer_logic as tm
from helpers.render_helper import custom_render


LOGIN_PARAMS = ('/auth', None)


@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def tm_start(request: HttpRequest) -> JsonResponse:
    """Start user workhours timer
    :todo: Investigate what's wrong with business_entity default value
    """

    data = json.loads(request.body)
    user_id = data.get('user_id', None)
    if not user_id:
      return JsonResponse({
        'result': 'error',
        'message': 'no user id specified'
      }, status=400)
    timer_message = tm.user_timer_start(user_id)
    return JsonResponse({
      'result': 'Ok',
      'message': timer_message
    }, status=200)


@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def tm_stop(request: HttpRequest) -> JsonResponse:
    """Stop user's active timer """

    user_id = request.POST.get('user_id', None)
    body = json.loads(request.body)
    if not user_id:
        user_id = request.user.id.id
    stop_timer = tm.user_timer_stop(user_id, data=body)
    return JsonResponse({
      'result': stop_timer['result'],
      'message': stop_timer['message']
    }, status=stop_timer['status'])


@require_http_methods(["DELETE"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def tm_cancel(request: HttpRequest) -> JsonResponse:
    """Delete user's active timer """

    user_id = request.user.id.id
    cancel_timer = tm.user_timer_cancel(user_id)
    return JsonResponse({
      'result': cancel_timer['result'],
      'message': cancel_timer['message']
    }, status=cancel_timer['status'])


def timer_page(request):
    return custom_render(
      request,
      'timer.html',
    )


@require_http_methods(["GET", "POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def tm_info(request: HttpRequest) -> JsonResponse:
    """A wrapper to call get/set on GET/POST"""

    if request.method == 'GET':
        return get_timer(request)
    elif request.method == 'POST':
        return set_timer(request)
    

@require_http_methods(["GET"])
def get_timer(request: HttpRequest) -> JsonResponse:
    """Get user's timer data """

    user_id = request.GET.get('user_id', None)
    if not user_id:
        user_id = request.user.id.id
    work_periods = tm.user_get_all_time_periods(user_id)
    return JsonResponse(work_periods, safe=False, status=200)


@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def set_timer(request: HttpRequest) -> JsonResponse:
    """Update user's timer data / including payments
    :todo: Seems extra-stale
    """

    user_id = request.GET.get('user_id', None)
    body = json.loads(request.body)
    if not user_id:
        user_id = request.user.id.id
    if not user_id:
      return JsonResponse({
        'result': 'error',
        'message': 'no user id specified'
      }, status=400)
    if request.method == 'POST':
        if not request.POST.get('ph'):
          return JsonResponse({
          'result': 'error',
          'message': 'no paid hours (ph) specified'
          }, status=400)
        if not request.POST.get('rate'):
          return JsonResponse({
          'result': 'error',
          'message': 'no rate specified'
          }, status=400)
    tm.user_timer_update(user_id, data=body)
    return JsonResponse({
      'result': 'Ok',
      'message': 'User info data saved successfully'
    }, status=200)


@require_http_methods(["GET", "POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def tm_current_status(request: HttpRequest) -> JsonResponse:
    timespans = tm.user_timer_currentstatus(request.user.id.id)
    status = 200
    return JsonResponse(
      {
        'time_spent_current_task': timespans['time_spent_current_task'],
        'time_spent_today_total': timespans['time_spent_today_total'],
      },
      status=status
    )
