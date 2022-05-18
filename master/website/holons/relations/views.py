import json
import logging

from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render

from email_api.helpers import auth_helper
from email_api.helpers import request_helper
from helpers import token_helper
from helpers.timer_helper import timer_setter

from accounts.models import User
from invitation.models import Token
from relations.models import Offer


def relations_index(request: HttpRequest) -> JsonResponse:
    data = {}
    return JsonResponse({
        'result': 'OK',
        'data': data,
    })
    

def relations_commitments(request: HttpRequest) -> JsonResponse:
    data = {}
    return JsonResponse({
        'result': 'OK',
        'data': data,
    })


