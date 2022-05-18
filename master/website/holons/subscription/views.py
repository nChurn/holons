import json
import logging

from django.conf import settings
from django.http import HttpRequest
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .services import stripe_payments as si
from helpers.render_helper import custom_render


subscription_type_plato = settings.SUBSCRIPTION_TYPE_PLATO 
subscription_type_early_adopt = settings.SUBSCRIPTION_TYPE_EARLY_ADOPT 
stripe_webhook_secret = settings.STRIPE_WH_SIGNING_SECRET


@require_http_methods(["GET"])
def index(request: HttpRequest) -> HttpRequest:
    return custom_render(
      request,
      'subscription/main.html',
    )


@require_http_methods(["GET"])
def list_subscriptions(request: HttpRequest) -> JsonResponse:
    """Return all active subscriptions for logged in user
    """

    if request.user.is_anonymous:
      return JsonResponse({
        'subscriptions': ''
      })
    subscriptions = si.get_active_subscriptions(request.user)
    return JsonResponse({'subscriptions': subscriptions,}, safe=False)


@require_http_methods(["POST",])
def create_customer(request: HttpRequest) -> JsonResponse:
    """Call Stripe API, ask to generate a Customer object
    to bind the subscription payments to (on the Stripe's side)
    """

    result = si.generate_stripe_customer_subscription(request.user)
    return JsonResponse(result)


@require_http_methods(["POST",])
def create_early_adopter(request: HttpRequest) -> JsonResponse:
    """Call our logic to create early adopter subscription
    """

    result = si.generate_stripe_customer_subscription(
        request.user,
        subscription_type=subscription_type_early_adopt
    )
    return JsonResponse(result)


@require_http_methods(["POST",])
def create_plato_customer(request: HttpRequest) -> JsonResponse:
    """Call our logic to create platos subscription
    """

    result = si.generate_stripe_customer_subscription(
        request.user,
        subscription_type=subscription_type_plato
    )
    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def wh_common(request: HttpRequest) -> JsonResponse:
    """Process Stripe incomming webhooks
    """

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    request_data = request.body
    if stripe_webhook_secret:
        event = si.get_stripe_event(request_data, sig_header, stripe_webhook_secret)
        event_type = event['type']
        data = json.loads(request_data)
    else:
        data = json.loads(request_data)
        event_type = request_data['type']
    if event.get('error', False) is True:
      return JsonResponse(
          {'message': event['message']}, status=event['status']
      )
    return JsonResponse(si.process_stripe_webhooks(event_type, data))


def cancel_subscription(request: HttpRequest, pk: str) -> JsonResponse:
    """Cancel Subscription
    """

    subscription_id = si.cancel_subscription_by_id(pk)
    return JsonResponse({
      'message': 'Subscription: ' + str(pk) + ' cancelled'
    })

        
def payment_failed(invoice_data: dict ) -> JsonResponse:
    pass

        
def subscription_deleted(invoice_data: dict ) -> JsonResponse:
    pass

