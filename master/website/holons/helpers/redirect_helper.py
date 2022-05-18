import logging

from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from email_api.helpers import auth_helper
from accounts.models import User


def perform_redirect(request: HttpRequest, vars = {}) -> HttpResponse:
    """Check if url has redirect_to argument, forward user to a given url

    e.g. /account?redirect_to=layers

    :param request:
    :param dict vars:
    :return: HttpResponse (200 if there's no redirect_to, 302 if token is present)
    """

    if auth_helper.get_user(request).id:
      redirect_to = request.GET.get('redirect_to', None)
      if redirect_to:
        response = redirect(redirect_to)
        # Example redirect to the Layers board invite
        # ?token=f29e079c-92f0-11eb-a93a-448a5bd87175&redirect_to=layers&project=131
        if 'layers' == redirect_to:
          prj_id = request.GET.get('project', None)
          token = request.GET.get('token', None)
          if prj_id:
            response['Location'] += '?project=' + str(prj_id)
            if token:
              response['Location'] += '&invite=' + str(token)
        else:
          response = redirect(redirect_to)
    else:
      '''
      :todo: that's a hack, will cause bugs for non-registered users
      '''
      response = redirect('/')
    return response
