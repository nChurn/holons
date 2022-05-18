import logging
import stripe

from datetime import datetime
from dateutil import tz
from django.conf import settings

from accounts.models import User
from subscription.models import EventLog
from subscription.models import Payment
from subscription.models import Subscription
from subscription.models import Card
from subscription.services.stripe_exceptions import EventAlreadyHappenedException


stripe.api_version = settings.STRIPE_API_VERSION
stripe.api_key = settings.STRIPE_SECRET_KEY
subscription_price = settings.SUBSCRIPTION_PRICE
subscription_product = settings.SUBSCRIPTION_PRODUCT_ID
subscription_price_id = settings.SUBSCRIPTION_PRICE_ID
subscription_length_days = settings.SUBSCRIPTION_LENGTH_DAYS
subscription_default_type = settings.SUBSCRIPTION_DEFAULT_TYPE
subscription_type_plato = settings.SUBSCRIPTION_TYPE_PLATO 
subscription_type_early_adopt = settings.SUBSCRIPTION_TYPE_EARLY_ADOPT 


def get_active_subscriptions(user: User) -> list:
    """Return active subscriptions for a given User
    """

    subscriptions_raw = user.subscriptions.filter(is_active=True).all()
    logging.info(f'subscriptions_raw: {subscriptions_raw}')
    subscriptions = []
    for el in subscriptions_raw:
      subscriptions.append({
        'id': str(el.id),
        'subscription_type': str(el.subscription_type),
        'expires_at': str(el.expires_at),
        'is_active': el.is_active,
      })
    return list(subscriptions)


def process_payment_intent_succeeded(payment_data: dict):
    """Process payment_intent.succeeded
    """

    try:
      _save_log(event_id=payment_data['id'],
                event_type='payment_intent.succeeded',
                event_data=payment_data)

    except EventAlreadyHappenedException:
      logging.info('event ' + payment_data['id'] + ' already happened, ignore')
      return
    # Update payment object based on customer_id
    payment = _save_payment(payment_data['data'])


def generate_stripe_customer_subscription(user: User,
                                          subscription_type: str = subscription_default_type
                                          ) -> dict:
    """Get Stripe client id, Stripe subscription object,
    append client secret and return as a single dict
    """

    stripe_cid = get_stripe_customer_id(user)
    subscription = create_subscription(user, stripe_cid)
    return {
      'customer_id': stripe_cid,
      'subscription_id': subscription.id,
      'client_secret': subscription.latest_invoice.payment_intent.client_secret
    }


def get_stripe_customer_id(user: User) -> str:
    """Get or create a Stripe customer, return their id
    """

    if user.subscriptions.first() is not None:
      try:
        logging.info(f'retrieve stripe customer')
        customer =_retrieve_stripe_customer_by_user(user)
      except stripe.error.InvalidRequestError:
        logging.info(f'create stripe customer')
        customer = _create_stripe_customer(user.email)
    else:
        logging.info(f'create stripe customer in ELSE')
        customer = _create_stripe_customer(user.email)
    customer_id = customer.get('id', None)
    return customer_id


def create_subscription(
      user: User,
      customer_id: str,
      subscription_type: str = subscription_default_type
    ) -> stripe.api_resources.subscription.Subscription:
    """Get Stripe customer_id for the User,
    Create Subscription
    Connect Subscription to the User
    """

    stripe_subscription = create_stripe_subscription(customer_id, subscription_type)
    local_subscription = create_local_subscription(user, customer_id, subscription_type, stripe_subscription)
    return stripe_subscription


def create_stripe_subscription(
      customer_id: str,
      subscription_type: str = subscription_default_type
    ) -> stripe.api_resources.subscription.Subscription:
    """Call Stripe, create Stripe subscription
    """

    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[{
            'price': subscription_price_id,
        }],
        payment_behavior='default_incomplete',
        expand=['latest_invoice.payment_intent'],
    )
    return subscription


def create_local_subscription(
      user: User,
      customer_id: str,
      subscription_type: str = subscription_default_type,
      stripe_subscription: stripe.api_resources.subscription.Subscription = None
    ):
    """Create local Subscription object, connect it to the User
    """

    expires_at = str(datetime.fromtimestamp(
      stripe_subscription.current_period_end, 
      tz=tz.gettz(settings.DEFAULT_TIMEZONE))
    )
    local_subscription = Subscription.objects.create(
      stripe_customer_id=customer_id,
      stripe_subscription_id=stripe_subscription.id,
      expires_at=expires_at,
      days_left=0,
    )
    user.subscriptions.add(local_subscription)


def get_stripe_event(request_data: dict, sig_header: str, webhook_secret: str) -> dict:
    """Call Stripe, register construct event
    """

    try:
        event = stripe.Webhook.construct_event(
          request_data, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return {
            'message': {'webhook processed': True,},
            'status': '400',
            'error': True,
        }
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return {
            'message': {'webhook processed': True,},
            'status': '400',
            'error': True,
        }
    return event


def process_stripe_webhooks(event_type: str, data: dict) -> dict:
    """Common Stripe incomming webhooks logic
    """

    if event_type == 'payment_intent.succeeded':
        logging.info('payment_intent.succeeded')
        process_payment_intent_succeeded(data)
    if event_type == 'invoice.paid':
        # Used to provision services after the trial has ended.
        # The status of the invoice will show up as paid. Store the status in your
        # database to reference when a user accesses your service to avoid hitting rate
        # limits.
        logging.info(f'invoice.paid')
        process_invoice_paid(data)

    if event_type == 'invoice.payment_failed':
        # If the payment fails or the customer does not have a valid payment method,
        # an invoice.payment_failed event is sent, the subscription becomes past_due.
        # Use this webhook to notify your user that their payment has
        # failed and to retrieve new card details.
        logging.info('invoice.payment_failed')
        # payment_failed(data)

    if event_type == 'customer.subscription.deleted':
        # handle subscription cancelled automatically based
        # upon your subscription settings. Or if the user cancels it.
        logging.info('customer.subscription.deleted')
        subscription_deleted(data)

    return {'webhook processed': True,}


def cancel_subscription_by_id(pk: str) -> str:
    """Cancel Subscription locally first,
    then ask Stripe to Delete Subscription 
    """

    local_subscription = Subscription.objects.filter(pk__exact=pk).get()
    local_subscription.is_active = False
    local_subscription.save()
    subscription = stripe.Subscription.delete(local_subscription.stripe_subscription_id)
    return str(pk)


def process_invoice_paid(invoice_data: dict):
    """Check and store payment based on invoice processed event

    * Get invoice event data
    * Try to create log record, exit if record exists,
    * Get Subscription by stripe customer_id
    * Create Payment object
    * Connect Payment to the Subscription 
    """

    try:
      _save_log(event_id=invoice_data['id'],  event_type='invoice.paid', event_data=invoice_data)

    except EventAlreadyHappenedException:
      logging.info('event ' + invoice_data['id'] + ' already happened, ignore')
      return
    # Update subscription object based on Stripe subscription data
    payment = _update_payment(invoice_data)


def _retrieve_stripe_customer_by_user(user: User):
    customer = stripe.Customer.retrieve(user.subscriptions.first().stripe_customer_id)
    return customer


def _create_stripe_customer(email: str):
    logging.info(f'create customer {email}')
    customer = stripe.Customer.create(
      email=email,
    )
    return customer


def _save_log(event_id: str='', event_type: str='', event_data: dict={}) -> bool:
    """Create new EventLog record,
    raise Exception if the record exists
    """

    log_record, created = EventLog.objects.get_or_create(
      event_id=event_id,
      event_type=event_type,
      event_data=event_data
    )
    if not created:
      raise EventAlreadyHappenedException('Event already processed')
    return True


def _update_payment(payment_data: dict) -> Payment:
    """Recieve Stripe invoice payment status,
    get payment_intent_id
    get local Subscription
    set Subscription days remaining
    set Subscription is_active
    append subscription to the Payment
    """

    invoice = payment_data['data']['object']
    payment_intent_id = invoice['payment_intent']
    subscription_id = invoice['subscription']
    subscription = Subscription.objects\
                    .filter(stripe_subscription_id=subscription_id)\
                    .first()
    payment = _get_or_create_payment(payment_intent_id)
    if invoice['status'] == 'paid':
        subscription.is_active = True
        subscription.days_left = subscription_length_days
        subscription.save()
    payment.subscription_id = subscription.id
    payment.save()
    return payment


def _save_payment(payment_data: dict) -> Payment:
    """Save successful payment data, attach it to the Subscription
    Set Subscription as active
    """

    invoice = payment_data['object']
    payment_intent_id = invoice['id']
    payment_method = invoice['charges']['data'][0]['payment_method']
    card_data = invoice['charges']['data'][0]['payment_method_details']['card']
    payment = _get_or_create_payment(payment_intent_id)
    card = _get_or_create_saved_card_info(card_data, payment_method, payment)
    payment.amount = invoice['amount']
    payment.status = invoice['status']
    payment.save()
    return payment


def _get_or_create_payment(payment_intent_id: str) -> Payment:
    """Get existing Payment
    or create a new Payment if there's no such object based on the payment_intent_id
    """

    payment = Payment.objects.filter(payment_intent=payment_intent_id).first()
    if payment is None:
        payment = Payment.objects.create(
            payment_intent=payment_intent_id,
        )
    return payment


def _get_or_create_saved_card_info(
        card_data: dict, payment_method: str, payment: Payment
    ) -> Card:
    """Get existing Card
    or create a new Card if there's no such object based on the fingerprint
    """

    card_fingerprint = card_data['fingerprint']
    last4 = card_data['last4']
    card_brand = card_data['brand']
    card = Card.objects.filter(card_fingerprint=card_fingerprint).first()
    if card is None:
        card = Card.objects.create(
            brand=card_brand,
            card_fingerprint=card_fingerprint,
            last4=last4,
            payment_method_id=payment_method,
        )
        payment.cards.add(card)
    return card
