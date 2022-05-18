import logging
import json
import requests

from django.conf import settings
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.middleware import csrf

from accounts.models import User
from social.address_book import update_social_graph
from invitation.models import Token
from email_api.helpers import request_helper
from email_api.helpers import auth_helper
from invitation import cookie as invitation_c
from rays import utilities as r_util



logging.basicConfig(level=logging.INFO)

TAIGA_API_URL = settings.TAIGA_API_URL
TAIGA_HEADERS = settings.TAIGA_HEADERS
TAIGA_ENABLED = True
TELEPORT_ENABLED = True
TELEPORT_API_URL = settings.TELEPORT_API_URL
API_HOSTNAME  = settings.LOGIN_API_HOSTNAME


@require_http_methods(["GET", "POST"])
def holons_login(request: HttpRequest) -> JsonResponse:
    """ Main login entry point / Also register new User

    * Get phone number
    * Call DB launcher, ask for confirmation
    * Get confirmation code
    * Save it to the local DB

    :param request: containing phone_number, username
    
    """

    data = json.loads(request.body)
    phone_number = data.get('phone_number', None)
    holons_user_name = data.get('username', None)
    if phone_number is None:
        return JsonResponse({'result': 'Not OK', 'message': 'no phone'})
    if holons_user_name is None:
        holons_user_name = 'holons_soul_' + phone_number
        holons_user_email = 'holons_soul_' + phone_number + '@holons.me'
    else:
        holons_user_email = holons_user_name.replace(' ', '.') + '@holons.me'

    url = API_HOSTNAME + '/public_api/send_confirmation_code'
    logging.info('Sending POST at ' + url)
    data = {'phone_number': phone_number, 'country': data.get('country', None)}

    r = requests.post(url, data=json.dumps(data), headers=TAIGA_HEADERS)
    confirmation_code = r.json()['confirmation_code']
    user = User.objects.filter(phone_number__exact=phone_number).first()
    print(user)
    print(data)
    if user is None:
        user = user_register(
          holons_user_email,
          holons_user_name,
          phone_number,
          confirmation_code,
          data.get('country', None)
        )
        update_social_graph(user)
    else:
        user.phone_confirmation_code = confirmation_code
        user.country = data.get('country', None)
        user.save()

    return JsonResponse({'result': 'OK'})


@require_http_methods(["GET", "POST"])
def holons_classic_login(request: HttpRequest) -> JsonResponse:
    """This is debug-only feature. Used to login using stale SMS code taken from DB.

    Works on localhost only

    :param request: containing phone_number, username
    """
    hostname = request.get_host()[:9]
    if 'localhost' != hostname:
        return JsonResponse({'result': 'Not OK', 'message': 'Login disabled'})
    if request.method == 'GET':
        return JsonResponse({'result': 'Not OK', 'message': 'Method not allowed'})
    elif request.method == 'POST':
        method = 'post'
    logging.info(request.POST.get('phone_number'))
    data = request.POST
    phone_number = data.get('phone_number', None)
    confirmation_code = data.get('confirmation_code', None)
    if phone_number is None:
        return JsonResponse({'result': 'Not OK', 'message': 'no phone'})

    user = User.objects.filter(phone_number__exact=phone_number).first()
    if user is None:
        logging.info('Classic login no such user')
        return JsonResponse({
          'result': 'Not OK',
          'message': 'Classic login no such user'
        })

    if phone_number == '' or confirmation_code == '':
        return JsonResponse({
          'result': 'Not OK',
          'message': 'no phone / confirmation code'
        })

    if confirmation_code == user.phone_confirmation_code:
        user.phone_confirmed = True
        user.is_active = True
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        user_status = 'not authenticated'
        if request.user.is_authenticated:
            logging.info('user authenticated')
            taiga_api_url = 'https://holons.me/boards/api/v1/'
            headers = {'Content-type': 'application/json'}
            # check if Taiga user exists
            # login them if exists
            login_data = {
                "password": "password_disabled",
                "type": "normal",
                "username": user.handle
            }
            r = requests.post(taiga_api_url + 'auth',
              data=json.dumps(login_data),
              headers=headers
            )
            logging.info('Taiga login:')
            logging.info(r.json())

            token = r.json()['auth_token']
            response = JsonResponse(
                {
                    'result': 'OK',
                    'check': 'OK',
                    'user_status': user_status,
                    'user_meta': r.json()
                }
            )
            user_status = 'authenticated'

        return redirect('/')


@require_http_methods(["POST"])
def confirmation(request: HttpRequest) -> JsonResponse:
    """Send request to the db.launcher.the.gt log in the user globally

    :param request: containing phone, confirmation_code
    """

    data = json.loads(request.body)
    phone_number = data['phone_number']
    confirmation_code = data['confirmation_code']
    if phone_number == '' or confirmation_code == '':
        return JsonResponse({
          'result': 'Not OK',
          'message': 'no phone / confirmation code'
        })

    user = User.objects.filter(phone_number__exact=phone_number).first()
    if not user:
        return JsonResponse({'result': 'Not OK', 'check': 'Not OK'})

    if confirmation_code == user.phone_confirmation_code:
        user.phone_confirmed = True
        user.is_active = True
        user.save()

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        logging.info('Successfully logged in to Django')

        if TELEPORT_ENABLED:
          logging.info('Logging into a teleport account')
          teleport_meta = teleport_user_auth(request, user)
        else:
          logging.info('Teleport is off')
          teleport_meta = 'Teleport is off'

        if TAIGA_ENABLED:
          response = taiga_login(request, user)
        else:
          response = dict(
              {
                  'result': 'OK',
                  'user_status': 'authenticated',
                  'workspaces_user_meta': 'Workspaces disabled',
              }
          )

        if teleport_meta:
          response['teleport_user_meta'] = teleport_meta

        r_util.set_default_rays(user)
        invitation_token = check_token(request, user)
        response['csrf_token'] = csrf.get_token(request)

        return JsonResponse(response)


def user_register(email: str, name: str, phone: str, confirmation_code: str, country: str) -> User:
    """Register new Django User

    :param email: User's email address
    :param name: username
    :param phone: user's phonenumber (numbers only)
    :param confirmation_code: SMS code
    """
    
    user, created = User.objects.get_or_create(
        username=name,
        defaults={
            'email': email,
            'first_name': '',
            'is_active': False,
            'is_staff': False,
            'is_superuser': False,
            'last_name': '',
            'name': name,
            'password': 'password_disabled',
            'phone_confirmed': False,
            'token': '',
            'country': country
        },
    )
    user.phone_number = phone
    user.phone_confirmation_code = confirmation_code
    user.country = country
    user.save()
    # @todo: process invitation_token cookie
    # @todo: add user to the social graph
    return user


def teleport_user_auth(request: HttpRequest, user: User) -> dict:
    """
    Check if user exists in Teleport
      Login the user to the Teleport
    Else
      Register a new user
    Login them to the Teleport
    """

    # check if Teleport user exists
    if teleport_user_not_exists(user):
      # create new Teleport user
      logging.info('Create new Teleport user')
      user_meta = teleport_user_register(user)
    else:
      # login them if exists
      logging.info('Login to Teleport')
      user_meta = teleport_user_login(user)

    logging.info('user_meta')
    logging.info(user_meta)
    return user_meta


def teleport_user_generate_username(user: User) -> str:
    """Generate unique Matrix user_id from email address
    Domain/matrix-server part is not taken into account here

    :returns: username
    :rtype: str 
    """

    return user.email.replace('@', '_at_')


def teleport_user_generate_password(user: User) -> str:
    """Self explanatory: generate a kind of dummy password
    for the Matrix Synapse account

    :todo: Disable Matrix password login in Synapse
    :returns: clear password
    :rtype: str 
    """

    return user.email.replace('@', '_at_') + '_password_disabled'


def teleport_user_login(user: User) -> dict:
    """Send User data to the Matrix API

    :param user: Django user object
    :return: auth-token dict from Matrix json response
    :rtype: dict
    """

    username = teleport_user_generate_username(user)
    password = teleport_user_generate_password(user) 

    login_data = {
      "type":"m.login.password",
      "identifier": {
        "type": "m.id.user",
        "user": username
      },
      "password": password
    }

    r = requests.post(TELEPORT_API_URL + 'login',
      data=json.dumps(login_data),
    )
    user = User.objects.filter(pk=user.id).first()
    user.cors_storage = r.json()
    user.save()
    return r.json()


def teleport_user_not_exists(user: User) -> bool:
    """Send User data to the Matrix API

    :param user: Django user object
    :return: True if username (phone_number) is occupied
    """

    username = teleport_user_generate_username(user)
    auth_url = TELEPORT_API_URL + 'register/available?username=' + username
    # What if the user has changed their Username after Teleport account was created?
    r = requests.get(auth_url)
    return r.json().get('available', False)


def teleport_user_register(user: User) -> dict:
    """
    Send User data to the Matrix API
    Register a new Teleport User
    Return auth-token
    """

    auth_url = TELEPORT_API_URL + 'register?kind=user'
    username = user.email.replace('@', '_at_')
    password = user.email.replace('@', '_at_') + '_password_disabled'
    user_data = {
      'username': username,
      'password': password
    }
    # Shall we call teleport_user_login after the registration?
    r = requests.post(auth_url, json.dumps(user_data))
    session = r.json().get('session', False)
    if session:
      user_data = {
        'username': username,
        'password': password,
        'initial_device_display_name':'teleport.holons.me',
        'auth':{
          'session': session,
          'type':'m.login.dummy'
        },
        'inhibit_login': False
      }
      r1 = requests.post(auth_url, json.dumps(user_data))
      user = User.objects.filter(pk=user.id).first()
      user.cors_storage = r1.json()
      user.save()
      return dict(r1.json())


def taiga_login(request: HttpRequest, user: User) -> dict:
    """Log in User to the Taiga
    Register them if no such user exists

    :todo: Default password hardcoded there is a DISASTER, fix it
    """

    user_status = 'not authenticated'
    if request.user.is_authenticated:
        logging.info('user authenticated')
        # check if Taiga user exists
        # login them if exists
        login_data = {
            "password": "password_disabled",
            "type": "normal",
            "username": user.email
        }
        r = requests.post(TAIGA_API_URL + 'auth',
          data=json.dumps(login_data),
          headers=TAIGA_HEADERS
        )
        # @todo: copy r.json to taiga_user
        token = r.json().get('auth_token', False)
        # if not create new Taiga user via REST-API
        # :todo: :fixme: I believe this will crash for the first ever login of the user,
        # :todo: investigate, create test
        if not token:
            # :todo: switch it from token to taiga_user
            token = taiga_register(user)
        return dict(
            {
                'result': 'OK',
                'check': 'OK',
                'user_status': 'authenticated',
                # @todo: insert taiga_user instead of r.json()
                # @todo: test it when done
                'workspaces_user_meta': r.json()
            }
        )


def taiga_register(user: User) -> str:
    """Take a Django User, register them in Taiga"""

    registration_data = {
        "accepted_terms": "true",
        "email": user.email,
        "full_name": user.username,
        "password": "password_disabled",
        "type": "public",
        "username": user.username
    }
    r = requests.post(TAIGA_API_URL + 'auth/register',
      data=json.dumps(registration_data),
      headers=TAIGA_HEADERS
    )
    logging.info('Taiga register')
    logging.info(r.json())

    return r.json()['auth_token']


def check_token(request: HttpRequest, user: User) -> bool:
    """
    Process invitation_token cookie
    """

    token_val = invitation_c.get_invitation_cookie(request)
    if not token_val:
      return False
    token_details = Token.objects.filter(value__exact=token_val).first()
    if token_details.token_type in ('invitation', 'offer')\
      and token_details.status == 'created':
      token_details.status = 'accepted'
      token_details.save()
      token_details.used_by.add(user.id)
      update_social_graph(token_details)
      return True

    return False


