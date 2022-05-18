import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from accounts.models import User
from relations.models import Offer
from relations.offers import format_offer


LOGIN_PARAMS = ('/auth', None)


"""List all user's Commitments  e.g. accepted offers
:TODO: rewrite the whole module analogous to moneta.buisiness_entities

e.g.
def crud():
    if request.method == 'GET':
      return _index(request)
etc
"""

@require_http_methods(["GET"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def index(request: HttpRequest) -> JsonResponse:
    """List all user's Offers
    """

    data = []
    user = request.user
    '''showing commitments'''
    commitments = user.offers_accepted.all()
    for offer in commitments:
      data.append(json.loads(format_offer(offer)))

    return JsonResponse({
        'result': 'OK',
        'data': data,
    })


