import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from helpers.profile_helper import get_account_status
from helpers.profile_helper import get_handle
from helpers.profile_helper import get_username
from helpers.profile_helper import get_userpic
from helpers.profile_helper import impersonate_accounts
from helpers.profile_helper import impersonate_menu_enabled
from helpers.profile_helper import get_balance_details
from helpers.profile_helper import get_user_logged_in_status
from helpers.redirect_helper import perform_redirect
from helpers.timer_helper import timer_setter
from invitation import cookie as invitation_c
from invitation.token import smart_redirect
from holons import restrictions


LOGIN_PARAMS = ('/auth', None)


def custom_render(request: HttpRequest, template: str, view_vars = {}) -> HttpResponse:
    """A wrapper for Django's renderer
    
    * Token-related logic
    * Attach user_timer to every response

    In case user is logged in and has invitation token,
    redirect them to the place the token says us to

    :todo: see if we can get rid of checking for template name in 'layers' redirect

    :return: HttpResponse (200 if there's no token, 302 if token is present)
    """

    user = request.user
    if request.user.is_anonymous:
      user_status = 'core'
    else:
      user_status = request.user.account_status

    '''
    NB: this is a-la paywall, add allowed urls to the holons.restrictions
    use ?skip-redirects=true in order to access any url
    '''

    redirect_counter = 0
    for allowed_url in restrictions.allowed_urls:
      redirect_counter += 1
      if '*' in allowed_url:
        if request.path.startswith(allowed_url.split('*')[0]):
          # :todo: mabe reverse if statement?
          logging.info(allowed_url.split('*')[0])
        elif redirect_counter == len(restrictions.allowed_urls):
          if request.user.is_anonymous or user_status == 'core':
            if request.path not in restrictions.allowed_urls\
              and not request.GET.get('skip-redirects')\
              and request.path != '/subscribe' and request.path != '/subscribe/':
                return redirect('/subscribe/')


    if request.GET.get('redirect_to', None):
      if request.path != '/' + str(request.GET.get('redirect_to', ''))\
        and request.path not in ('/index', '/auth'):
        return perform_redirect(request)

    view_vars['user_timer'] = timer_setter(request)
    view_vars['userpic'] = get_userpic(request)
    view_vars['username'] = get_username(request)
    view_vars['account_status'] = get_account_status(request)
    view_vars['handle'] = get_handle(request)
    view_vars['impersonate_menu_enabled'] = impersonate_menu_enabled(request)
    view_vars['balance_data'] = get_balance_details(request)
    view_vars['user_logged_in'] = get_user_logged_in_status(request)
    if impersonate_menu_enabled(request):
      view_vars['impersonate_accounts'] = impersonate_accounts(request)
    response = render(request, template, view_vars)
    token = request.GET.get('token', None)

    if 'layers' in template:
      layers_invite = request.GET.get('invite', None)
      if layers_invite and not user.is_authenticated:
        return smart_redirect(request, layers_invite)
    if user.is_authenticated:
      token_cookie_val = invitation_c.get_invitation_cookie(request)
      if token_cookie_val or token:
        return smart_redirect(request, token)
    elif token:
      ''' move token from URL to the cookie '''
      response = invitation_c.set_invitation_cookie(response, token)
    return response

