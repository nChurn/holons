import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from helpers.render_helper import custom_render
from accounts.models import User
from relations.models import Offer
from relations.models import Invoice


LOGIN_PARAMS = ('/auth', None)


"""List all user's Invoices
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
    """List all user's Invoices
    """

    data = []
    user = request.user
    '''showing invoices'''
    offers_accepted = user.offers_accepted.all()
    for offer in offers_accepted:
      invoices = offer.invoices.all()
      for invoice in invoices:
        data.append(json.loads(format_invoice(invoice)))
    invoices = user.invoices_accepted.all()
    for invoice in invoices:
        data.append(json.loads(format_invoice(invoice)))

    return JsonResponse({
        'result': 'OK',
        'data': data,
    })


@require_http_methods(["GET"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def show(request: HttpRequest, pk: str) -> JsonResponse:
    invoice = Invoice.objects.filter(pk=pk).get()
    data = json.loads(format_invoice(invoice))

    return JsonResponse({
        'result': 'OK',
        'data': data,
    })
    

@require_http_methods(["GET"])
def show_invoice(request: HttpRequest, pk: str) -> HttpResponse:
    invoice = Invoice.objects.filter(pk=pk).get()
    data = json.loads(format_invoice(invoice))

    return custom_render(
      request,
      'relations/invoice.html',
      {'invoice_data': json.dumps(data)}
    )


@require_http_methods(["POST"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def create(request: HttpRequest) -> JsonResponse:
    """Creates a new Invoice object
    """

    data = json.loads(request.body)
    offer_id = data.get('id', None)
    title = data.get('title', None)
    from_name = data.get('from_name', None)
    to_name = data.get('to_name', None)
    status = 'created'
    is_paid = False
    amount = data.get('invoice_amount', None)
    
    user = request.user

    if not offer_id:
      return JsonResponse({'result': 'error', 'message': 'empty offer_id'}, status=400)
    if not title:
      return JsonResponse({'result': 'error', 'message': 'empty title'}, status=400)
    if not from_name:
      return JsonResponse({'result': 'error', 'message': 'empty from_name'}, status=400)
    if not to_name:
      return JsonResponse({'result': 'error', 'message': 'empty to_name'}, status=400)
    if not amount:
      return JsonResponse({'result': 'error', 'message': 'empty amount'}, status=400)


    invoice = Invoice.objects.create(
      title = title,
      from_name = from_name,
      to_name = to_name,
      status = status,
      is_paid = is_paid,
      amount=amount,
    )
    invoice.owner.add(user.id)
    offer = Offer.objects.filter(pk=offer_id).first()
    offer.invoices.add(invoice)
    offer.save()

    return JsonResponse({
        'result': 'OK',
        'data': json.loads(format_invoice(invoice)),
    })


@require_http_methods(["PATCH"])
@login_required(login_url=LOGIN_PARAMS[0], redirect_field_name=LOGIN_PARAMS[1])
def accept(request: HttpRequest, pk) -> JsonResponse:
    """Accept an Invoice object
    """

    data = json.loads(request.body)
    from_name = data.get('fromName', None)
    to_name = data.get('toName', None)
    status = data.get('status', None)
    
    user = request.user
    invoice = Invoice.objects.filter(pk=pk).get()

    invoice.status = 'accepted'
    invoice.is_accepted = True
    invoice.accepted_by.add(request.user)

    invoice.save()

    return JsonResponse({
        'result': 'OK',
        'message': 'Offer edited',
        'data': json.loads(format_invoice(invoice)),
    })

def format_invoice(invoice: Invoice) -> json:
    accepted_by = 'Not accepted'
    if len(invoice.accepted_by.all()) > 0:
      accepted_by = str(invoice.accepted_by.all().first().username)
    invoice = {
      'id': str(invoice.id),
      'title': invoice.title,
      'from_name': invoice.from_name,
      'to_name': invoice.to_name,
      'amount': str(invoice.amount),
      'accepted_by': accepted_by,
      'is_paid': invoice.is_paid,
    }
    return json.dumps(invoice)
