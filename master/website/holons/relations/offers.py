import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helpers import token_helper
from helpers.render_helper import custom_render
from accounts.models import User
from invitation.models import Token
from relations.models import Offer


LOGIN_PARAMS = ('/auth', None)


"""List all user's Offers
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
    '''showing offers'''
    offers = user.offers\
      .exclude(status='withdrawn')\
      .exclude(status='accepted')
    # :TODO: matching by user.phone_numbers seems crazy
    # how could we improve Offer data?
    # use M2M?
    incomming_offers = offers\
      .filter(to_name__endswith=user.phone_number)\
      .exclude(status='withdrawn')\
      .exclude(status='accepted')
    accepted_offers = user.offers_accepted.all()
    for offer in accepted_offers:
      data.append(json.loads(format_offer(offer)))
    for offer in incomming_offers:
      data.append(json.loads(format_offer(offer)))
    for offer in offers:
      data.append(json.loads(format_offer(offer)))

    return JsonResponse({
        'result': 'OK',
        'data': data,
    })


@require_http_methods(["GET"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def get_by_token(request: HttpRequest, invite_token: str) -> JsonResponse:
    offer = Offer.objects.filter(invite_token=invite_token).get()
    data = json.loads(format_offer(offer))

    return JsonResponse({
        'result': 'OK',
        'data': data,
    })

@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def show(request: HttpRequest, pk: int) -> JsonResponse:
    """Seems stale
    :TODO: test and remove this method
    """

    user = request.user
    data = json.loads(request.body)
    '''accept offer'''
    offer = Offer.objects.filter(to_name__endswith=user.phone_number).filter(pk=pk).get()
    if data.get('status', None) == 'accepted':
      offer.status = 'accepted'
      offer.save()
      data = json.loads(format_offer(offer))

    return JsonResponse({
        'result': 'OK',
        'data': data,
    })

# @require_http_methods(["GET"])
def show_offer(request: HttpRequest, invite_token: str) -> HttpResponse:
    offer = Offer.objects.filter(invite_token=invite_token).get()
    data = json.loads(format_offer(offer))

    return custom_render(
      request,
      'relations/offer.html',
      {'offer_data': json.dumps(data)}
    )

# @require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def create(request: HttpRequest) -> JsonResponse:
    """Creates a new Offer object
    """

    data = json.loads(request.body)
    title = data.get('contractTitle', None)
    from_name = data.get('fromName', None)
    to_name = data.get('toName', None)
    terms_from = data.get('termsFrom', None)
    terms_to = data.get('termsTo', None)
    consideration = data.get('consideration', None)
    timeframe = data.get('timeframe', None)
    status = 'created'
    is_accepted = False
    paragraphs = data.get('paragraphs', None)
    contract_type = data.get('contractType', 'generic')
    is_membership_sponsor = data.get('membershipSponsor', False)
    
    user = request.user

    if not title:
      return JsonResponse({'result': 'error', 'message': 'empty title'}, status=400)
    if not from_name:
      return JsonResponse({'result': 'error', 'message': 'empty from_name'}, status=400)
    if not to_name:
      return JsonResponse({'result': 'error', 'message': 'empty to_name'}, status=400)
    if not terms_from:
      return JsonResponse({'result': 'error', 'message': 'empty terms_from'}, status=400)
    if not terms_to:
      return JsonResponse({'result': 'error', 'message': 'empty terms_to'}, status=400)
    if not consideration:
      return JsonResponse({'result': 'error', 'message': 'empty consideration'}, status=400)
    if not timeframe:
      return JsonResponse({'result': 'error', 'message': 'empty timeframe'}, status=400)

    token = Token.objects.create(
      value=token_helper.token_generate(delimiter='-'),
      token_type='offer',
      status='created'
    )
    token.issuer.add(user.id)

    offer = Offer.objects.create(
      title = title,
      from_name = from_name,
      to_name = to_name,
      terms_from = terms_from,
      terms_to = terms_to,
      consideration = consideration,
      timeframe = timeframe,
      invite_token = token.value,
      status = status,
      is_accepted = is_accepted,
      paragraphs = paragraphs,
      contract_type = contract_type,
      is_membership_sponsor = is_membership_sponsor,
    )
    offer.owner.add(user.id)
    offer_json = format_offer(offer)

    return JsonResponse({
        'result': 'OK',
        'data': json.loads(offer_json),
    })


@require_http_methods(["DELETE"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def delete(request: HttpRequest, pk) -> JsonResponse:
    """Delete an Offer object
    """

    offer = Offer.objects.filter(pk=pk).get()
    offer.status = 'withdrawn'
    offer.save()

    return JsonResponse({
        'result': 'OK',
        'message': 'Offer withdrawn',
        'data': {
          'offer_id': str(offer.id),
          'status': offer.status,
        },
    })


@require_http_methods(["PATCH"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def accept(request: HttpRequest, pk) -> JsonResponse:
    """Accept an Offer object
    """

    data = json.loads(request.body)
    logging.info(data)
    logging.info(pk)
    # invite_token = data.get('inviteToken', None)
    # status = data.get('status', None)
    
    user = request.user
    offer = Offer.objects.filter(pk=pk).get()
    logging.info(offer)

    offer.status = 'accepted'
    offer.is_accepted = True
    offer.accepted_by.add(request.user)

    offer.save()
    offer_json = format_offer(offer)

    return JsonResponse({
        'result': 'OK',
        'message': 'Offer edited',
        'data': json.loads(offer_json),
    })


@require_http_methods(["PATCH"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def edit(request: HttpRequest, pk) -> JsonResponse:
    """Edit an Offer object
    """

    data = json.loads(request.body)
    contract_title = data.get('contractTitle', None)
    from_name = data.get('fromName', None)
    to_name = data.get('toName', None)
    terms_from = data.get('termsFrom', None)
    terms_to = data.get('termsTo', None)
    consideration = data.get('consideration', None)
    timeframe = data.get('timeframe', None)
    invite_token = data.get('inviteToken', None)
    status = data.get('status', None)
    is_accepted = data.get('isAccepted', None)
    paragraphs = data.get('paragraphs', None)
    
    user = request.user
    offer = Offer.objects.filter(pk=pk).get()

    offer.contract_title = contract_title
    offer.from_name = from_name
    offer.to_name = to_name
    offer.terms_from = terms_from
    offer.terms_to = terms_to
    offer.consideration = consideration
    offer.timeframe = timeframe
    offer.status = status
    # offer.is_accepted = is_accepted
    offer.paragraphs = paragraphs

    offer.save()
    offer_json = format_offer(offer)

    return JsonResponse({
        'result': 'OK',
        'message': 'Offer edited',
        'data': json.loads(offer_json),
    })


def format_offer(offer: Offer) -> json:
    return json.dumps({
      'id': str(offer.id),
      'title': offer.title,
      'from_name': offer.from_name,
      'to_name': offer.to_name,
      'terms_from': offer.terms_from,
      'terms_to': offer.terms_to,
      'consideration': offer.consideration,
      'timeframe': offer.timeframe,
      'invite_token': offer.invite_token,
      'status': offer.status,
      'is_accepted': offer.is_accepted,
      'paragraphs': offer.paragraphs,
      'created_at': str(offer.created_at),
      'is_membership_sponsor': str(offer.is_membership_sponsor),
    })


@require_http_methods(["POST"])
def render(request: HttpRequest, invite_token: str) -> HttpResponse:
    """
    :TODO: get rid of this method (we reimplement it in show_offer)
    Redirect anonymous user to the auth
    or
    Show offer based on token to the authorised user
    """

    ''' check if user is logged in '''
    if request.user.is_anonymous:
      response = redirect('/auth?token=' + invite_token)
      return response

    ''' if user is logged in, show them the Offer '''
    ''' render offer '''
    offer = Offer.objects.filter(invite_token=invite_token).get()
    data = json.loads(format_offer(offer))

    user_timer = timer_setter(request)
    return render(request, 'relations/relations.html', {'user_timer': user_timer})

