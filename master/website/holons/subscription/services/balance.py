import logging
import json

from django.conf import settings

from accounts.models import User
from subscription.models import Subscription


class Balance:
  """All things balance-related
  e.g. account is paid, when the next payment is due etc
  :todo: THink it over, it looks like it belongs to the models world
  """


  def __init__(self, user: User):
      self.user = user
      if user.is_authenticated:
        self.subscription = self.user.subscriptions.filter(is_active=True).last()
      else:
        self.subscription = Subscription.objects.create()



  def account_is_paid(self) -> bool:
      """Decide if the account is commercial and active"""
      if self.subscription:
        return True
      else:
        return False



  def amount(self) -> float:
      """Count and return total active credits for the user"""
      return 1.1


  def next_payment(self) -> str:
      """Get next subscription payment date"""
      if self.subscription:
        return self.subscription.expires_at


  def paid_by(self) -> str:
      """Get subscription sponsor"""
      return '@grintender'

  def subscription_title(self) -> str:
      if self.subscription:
        return self.subscription.subscription_type
      return ''
