import json
import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import BusinessEntity


LOGIN_PARAMS = ('/auth', None)




@require_http_methods(["GET", "POST", "PATCH", "DELETE"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def crud(request: HttpRequest) -> JsonResponse:
    """
    Kind of a CRUD router to orchestrate CREATE, EDIT, DELETE
    Entities, based on an HTTP-request method

    :return:
    """
    method = ''
    if 'GET' == request.method:
      return _index(request)
    if 'POST' == request.method:
      return _create(request)
    if 'PATCH' == request.method:
      method = 'patch'
    if 'DELETE' == request.method:
      method = 'delete'


    return JsonResponse({
        'result': 'OK',
        'method': method,
    })


def _create(request: HttpRequest) -> JsonResponse:
    """Create a new BusinessEntity
    :return:
    """
    data = json.loads(request.body)
    name = data.get('name', None)
    if not name:
      return JsonResponse({'result': 'error', 'message': 'empty name'}, status=400)

    be = BusinessEntity.objects.create(name=name)
    request.user.entities.add(be)
    return JsonResponse({
        'result': 'OK',
        'message': 'Entity created',
    })
  

def _index(request: HttpRequest) -> JsonResponse:
    """ List all BusinessEntities available to the user
    :return:
    """

    entities = request.user.entities.all()
    result = []
    for el in entities:
      logging.info(el)
      result.append({
        'id': str(el.id),
        'name': el.name
      })

    return JsonResponse({
        'result': 'OK',
        'entities': result,
    })
