import json
import requests

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import login
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from helpers.profile_helper import impersonate_accounts
from helpers.profile_helper import impersonate_menu_enabled
from helpers.render_helper import custom_render
from helpers.profile_helper import get_bio
from accounts.models import User


LOGIN_PARAMS = ('/auth', None)


@require_http_methods(['GET'])
def user_profile(request: HttpRequest, handle: str = '') -> HttpResponse:
    if request.user.is_authenticated:
      return user_profile_own(request)
    """Render common users's profile, accessible to every Holons person"""
    user = User.objects.filter(handle=handle).first()
    if not user:
      return render(request, '404.html', status=404)
    else:
      # skip profile_handler
      return custom_render(
        request,
        'profile-plain.html',
        {
          'profile_handle': user.handle, 
          'profile_username': user.username, 
          'profile_userpic': user.userpic.url, 
          'profile_bio': user.bio
        }
      )


@require_http_methods(['GET'])
def user_profile_own(request: HttpRequest) -> HttpResponse:
    """Render current user's editable profile page"""

    return custom_render(
      request,
      'profile-plain-own.html',
      {
        'bio': get_bio(request)
      }
    )

@require_http_methods(['GET'])
def user_impersonate(request: HttpRequest, phone_number: str) -> HttpResponse:
    """Logout current user, login a new one, based by the phone_number

    * Check if the user has rights to switch profile
    * Check if the phone_number is in the awailable profiles list
    * Logout current user
    * Login a new selected user

    """
    redirect_to = request.GET.get('redirect_to', None)
    if not impersonate_menu_enabled(request):
      return redirect('/')
    new_user = User.objects.filter(phone_number=phone_number).first()
    check_user = {'username': new_user.username, 'phone_number': new_user.phone_number}
    if check_user in impersonate_accounts(request):
      logout(request)
      login(request, new_user)
    else:
      logging.info('Not OK')
      return redirect('/')

    return redirect(redirect_to)
      
    
    
