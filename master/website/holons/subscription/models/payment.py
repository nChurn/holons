from django.db import models
from django.contrib import admin

from djmoney.models.fields import MoneyField
from hashid_field import HashidAutoField
from django_jsonfield_backport.models import JSONField

from accounts.models import User
from .subscription import Subscription


class Payment(models.Model):
    """Single payment record"""

    id = HashidAutoField(primary_key=True)
    subscription = models.ForeignKey(
        Subscription, blank=True, null=True, default=None,
        on_delete=models.CASCADE,
        verbose_name='Subscription for which we are paying'
    )
    amount = MoneyField(
        max_digits=14, decimal_places=2, default_currency='USD',
        blank=True, null=True, default=None,
        verbose_name='How much do we pay'
    )
    payment_intent = models.CharField(
        max_length=255, unique=False, default='',
        verbose_name='Payment intent id inside Stripe'
    )
    status = models.CharField(
        max_length=255, unique=False, default='fail',
        verbose_name='Was the payment successful?'
    )
    created_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(
        auto_now=True, blank=True, null=True
    )

    def __str__(self):
        return str(self.id) 

    def __unicode__(self):
        return str(self.id) 
