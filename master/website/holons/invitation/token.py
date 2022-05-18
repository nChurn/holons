import logging
from django.shortcuts import redirect
from django.http import HttpRequest, HttpResponse
from email_api.helpers import auth_helper
from invitation import cookie as invitation_c
from .models import Token

def smart_redirect(request: HttpRequest, token: str = '', delete_token_cookie: bool = True) -> HttpResponse:
    """Route user to the URL's based on token type

    * get token value 
    * access token DB model 
    * find out what this token is for 
    * get redirect path 
    * depending on token type we could also change token parameters 
    * prepare redirect 
    * find out if we need to delete token cookie 

    :param request: HttpRequest
    :param token: str
    :param delete_token_cookie: bool

    """
    
    redirect_to = '/'
    token_val = invitation_c.get_invitation_cookie(request)
    if token:
      token_val = token
    if token_val:
      token_details = Token.objects.filter(value__exact=token_val).first()
      token_type = token_details.token_type 
      if token_type == 'offer':
        redirect_to = '/relations/offers/' + token_details.value
      if token_type == 'invitation':
        redirect_to = '/auth?token=' + token_details.value
      if token_type == 'layers':
        prj_id = request.GET.get('project', None)
        redirect_to = '/auth?token=' + token_details.value + '&redirect_to=layers&project=' + prj_id
    if delete_token_cookie:
      return invitation_c.delete_invitation_cookie(redirect(redirect_to))
    else:
      return redirect(redirect_to)

def token_change_status(token_str: str, status: str = 'used') -> bool:
    """Change invitation-token object in the DB

    :param token_str: str
    :param status: str
    :returns: bool
    """

    token = Token.objects.filter(value__exact=token_str).first()
    if token:
      token.status = status
      token.save()
      return True
    return False
