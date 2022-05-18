from django.http import HttpRequest, HttpResponse

def set_invitation_cookie(response: HttpResponse, token: str) -> HttpResponse:
  response.set_cookie('holons_invitation', token)
  return response

def get_invitation_cookie(request: HttpRequest) -> str:
  try:
    token = request.COOKIES['holons_invitation']
  except KeyError:
    token = ''
  return token

def delete_invitation_cookie(response: HttpResponse) -> HttpResponse:
  response.delete_cookie('holons_invitation')
  return response
