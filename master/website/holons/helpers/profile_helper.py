import logging

from django.conf import settings
from django.http import HttpRequest
from django.http import HttpResponse

from accounts.models import User
from subscription.services.balance import Balance


def get_userpic(request: HttpRequest) -> str:
    """Get user's userpic
    :return: Userpic URL
    """
    
    userpic = settings.DEFAULT_USERPIC
    if not request.user.is_anonymous and request.user.userpic:
        userpic = request.user.userpic.url
        # userpic = request.user.userpic.url.replace('/usg/usg/', '/usg/')

    return userpic


def get_username(request: HttpRequest) -> str:
    """Get username of the logged in user
    :return: 
    """

    username = ''
    if not request.user.is_anonymous:
      username = request.user.username
    return  username


def get_handle(request: HttpRequest) -> str:
    """Get user's handle
    :return:
    """

    handle = ''
    if not request.user.is_anonymous:
       handle = request.user.handle
    if handle == '':
      handle = 'soul_' + str(request.user.id)
    return handle


def get_user_logged_in_status(request: HttpRequest) -> str:
    """Get user's account_status
    :return:
    """

    if not request.user.is_anonymous:
       return True
    return False


def get_account_status(request: HttpRequest) -> str:
    """Get user's account_status
    :return:
    """

    account_status = ''
    if not request.user.is_anonymous:
       account_status = request.user.account_status
    if account_status == '':
      account_status = 'classic'
    return account_status


def get_bio(request: HttpRequest) -> str:
    """Get user's handle
    :return:
    """

    bio = ''
    if not request.user.is_anonymous:
       bio = request.user.bio
    return bio


def impersonate_menu_enabled(request: HttpRequest) -> bool:
    """Check if the user has access to a profile-switcher menu
    :todo: Get rid of the hard-code, after we introduce roles
    """
    if not request.user.is_anonymous \
      and request.user.phone_number in settings.IMPERSONATE_MENU_AVAILABLE_TO:
      return True
    return False


def impersonate_accounts(request: HttpRequest) -> list:
    """A place to generate profile-switcher items available to the user"""
    logging.info(request.user)

    accounts = []
    for phone_number in settings.IMPERSONATE_PROFILES:
      user_data = User.objects.filter(phone_number=phone_number).first()
      if user_data:
        accounts.append({
          'username': user_data.username,
          'phone_number': user_data.phone_number, 
        })
    return accounts


def get_balance_details(request: HttpRequest) -> dict:
    """Entry point to all things money about the user-account

    e.g. subscription price, next payment date, who pays for you etc.
    :todo: is there a more pythonic, django-way to work with balance data?

    :return: dict
    """

    balance = Balance(request.user)

    balance_details = {
      'paid_account': balance.account_is_paid,
      'amount': balance.amount,
      'currency': '$',
      'period': 'monthly',
      'period_pay': settings.SUBSCRIPTION_PRICE/100,
      'next_payment': balance.next_payment,
      'paid_by': balance.paid_by,
      'subscription_title': balance.subscription_title,
    }
    return balance_details
