import logging
import json
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from email_api.helpers import request_helper
from email_api.helpers import auth_helper
from helpers import token_helper
from accounts.models import User
from invitation.models import Token


def invitation_generate_code(request: HttpRequest) -> JsonResponse:
    """
    Used to generate, save and send over AJAX invitation token
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    token = Token.objects.create(
      value=token_helper.token_generate(delimiter='-'),
      token_type='invitation',
      status='created'
    )
    token.issuer.add(user.id)
    data = {
      'code': token.value
    }
    return JsonResponse({
        'result': 'OK',
        'method': method,
        'data': data,
    })

    
def generate_layers_invite(request: HttpRequest) -> JsonResponse:
    """
    Used to store Taiga generated invitation code into Holons DB
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    token_str = data['token']
    token = Token.objects.create(
      value=token_str,
      token_type='layers',
      status='created'
    )
    token.issuer.add(user.id)
    token.save()
    data = {
      'code': token.value
    }
    return JsonResponse({
        'result': 'OK',
        'method': method,
        'data': data,
    })
    
