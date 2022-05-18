import logging

from social.serializers import UserSerializer

from django.conf import settings
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from social.address_book import get_address_book

from accounts.models import User


@require_http_methods(["GET"])
@login_required
def address_book(request: HttpRequest) -> dict:
    # return UserSerializer(User.objects.filter(handle__in=RAY_SOURCES).all() + request.user.social.all(), many=True)
    return JsonResponse(UserSerializer(User.objects.all(), many=True).data, safe=False)