import logging
import json
import requests
import magic 

from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from accounts.models import User
from accounts.views import taiga_login
from accounts.views import teleport_user_auth
from email_api.helpers import request_helper
from email_api.helpers import auth_helper
from invitation import cookie as invitation_c


TAIGA_API_URL = settings.TAIGA_API_URL
TAIGA_HEADERS = settings.TAIGA_HEADERS
TELEPORT_API_URL = settings.TELEPORT_API_URL
LOGIN_PARAMS = ('/auth', None)


@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def edit(request: HttpRequest) -> JsonResponse:
    """Recieve changes from UI, update profile as necessary

    :param request:
    :return: JsonResponse
    """

    result = ''
    data = json.loads(request.body)

    handle = data.get('handle', None)
    username = data.get('username', None)
    bio = data.get('bio', None)
    if username:
      result += "Username changed \n"
      _change_username(username, request.user)
      response = {'result': result}
      st_code = 200
    if handle:
      result += 'Handle changed \n'
      _change_handle(handle, request.user)
      response = {'result': result}
      st_code = 200
    if bio:
      result += 'Bio changed \n'
      _change_bio(bio, request.user)
      response = {'result': result}
      st_code = 200
    if result == '':
      result = 'Profile not edited'
      response = {'result': result}
      st_code = 200
    fresh_user = User.objects.filter(pk=request.user.id).first()
    response['user'] = {
      'username': fresh_user.username,
      'handle': fresh_user.handle,
      'bio': fresh_user.bio,
    }
    return JsonResponse(response, status=st_code)


def _change_username(username: str, user: User):
    user.username = username
    user.save()

def _check_handle_exists(handle: str, user: User) -> str:
    """Check if such handle already is taken
    Append user.hashid to handle, if necessary
    """
    check_user = User.objects.filter(handle=handle)
    if check_user.count() > 0\
      and check_user.filter(pk=user.id).first() is None:
      handle = handle + '_' + str(user.id)
    return handle

def _change_handle(handle: str, user: User):
    handle = _check_handle_exists(handle, user)
    user.handle = handle
    user.save()


def _change_bio(bio: str, user: User):
    user.bio = bio
    user.save()


def _update_taiga_userpic(request: HttpRequest) -> JsonResponse:
    """Feed uploaded Django User avatar to Taiga API"""
    taiga_user = _get_taiga_user_creds(request)
    taiga_avatar_url = TAIGA_API_URL + 'users/change_avatar'
    taiga_headers = {}
    taiga_headers['Authorization'] = 'Bearer ' + taiga_user['workspaces_user_meta']['auth_token']
    file_object = {'avatar': open(request.user.userpic.path, 'rb')}
    r = requests.post(taiga_avatar_url,
      headers=taiga_headers,
      data=[],
      files=file_object,
    )


def _get_taiga_user_creds(request: HttpRequest) -> dict:
    """Log in User to the Taiga
    Get user credentials
    """

    taiga_token = taiga_login(request, request.user)
    return taiga_token


def _update_teleport_userpic(request: HttpRequest) -> JsonResponse:
    """Feed uploaded Django User avatar's URr to Matrix Synapse API"""
    teleport_user = _get_teleport_user_creds(request)
    teleport_avatar_url = TELEPORT_API_URL + 'profile/'+ teleport_user['user_id'] + '/avatar_url'
    teleport_headers = {}
    teleport_headers['Authorization'] = 'Bearer ' + teleport_user['access_token']
    teleport_uploaded_avatar_uri = _upload_teleport_avatar(request, teleport_user, teleport_headers)
    r = requests.put(teleport_avatar_url,
      headers=teleport_headers,
      data=json.dumps({'avatar_url': teleport_uploaded_avatar_uri}),
    )
    for el in r:
      logging.info(el)
    logging.info(r.json())
    pass


def _get_teleport_user_creds(request: HttpRequest) -> dict:
    """Log in User to the Teleport
    Get user credentials
    """

    teleport_creds = teleport_user_auth(request, request.user)
    return teleport_creds

def _upload_teleport_avatar(request: HttpRequest, teleport_user: dict, teleport_headers: dict) -> str:
    """Upload Django userpic, get Matrix msc:// url

    :return: mxc:// Matrix Synapse content repository url to the uploaded file
    """

    mime = magic.from_file(request.user.userpic.path, mime=True)
    teleport_headers['Content-Type'] = mime
    teleport_upload_url = TELEPORT_API_URL.replace('client', 'media')\
      + 'upload?filename=avatar.' + mime.split('/')[1]
    r = requests.post(teleport_upload_url,
      headers=teleport_headers,
      data=open(request.user.userpic.path, 'rb').read()
    )
    return json.loads(r.text)['content_uri']
    

@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def picture_upload(request: HttpRequest) -> JsonResponse:
    """Recieve a file from UI, store it and then:

    * update profile
    * push new picture to the Taiga
    * push new picture to the Teleport

    :param request:
    :return: JsonResponse
    """

    user = request.user
    ''' Upload picture to django User '''
    if 'userpic' in request.FILES:
      user.userpic = request.FILES['userpic'] 
      user.save()
    else:
      return JsonResponse({'result': 'No image data'}, status=400)

    _update_taiga_userpic(request)
    _update_teleport_userpic(request)


    response = {
      'result': 'Picture upload OK',
      'image-src': str(user.userpic.url)
    }
    return JsonResponse(response, status=200)
