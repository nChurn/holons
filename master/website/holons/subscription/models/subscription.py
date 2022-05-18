from django.db import models
from django.contrib import admin

from djmoney.models.fields import MoneyField
from hashid_field import HashidAutoField
from django_jsonfield_backport.models import JSONField

from accounts.models import User


class Subscription(models.Model):
    """Main subscription data

      * who
      * what
      * when
      * how much
    """

    id = HashidAutoField(primary_key=True)
    owner = models.ManyToManyField(
        User, related_name='subscriptions', blank=True,
        verbose_name='Who is using this subscription'
    )
    subscription_type = models.CharField(
        max_length=255, unique=False, default='holons core',
        verbose_name='String, identifiyng what is this subscription for (core service, plato etc...)'
    )
    is_active = models.BooleanField(
        default=False,
        verbose_name='Is subscription active'
    )
    created_at = models.DateTimeField(
        auto_now=True, blank=True, null=True
    )
    expires_at = models.DateTimeField(
        auto_now=False, blank=True, null=True, default=None,
        verbose_name='Last active day of the subscription'
    )
    next_charge_at = models.DateTimeField(
        auto_now=False, blank=True, null=True, default=None,
        verbose_name='When the client\'s card will be charged again'
    )
    stripe_customer_id = models.CharField(
        max_length=255, unique=False, default='',
        verbose_name='Customer id inside Stripe'
    )
    stripe_subscription_id = models.CharField(
        max_length=255, unique=False, default='',
        verbose_name='Subscription id inside Stripe'
    )
    days_left = models.IntegerField(
        default=0, null=True,
        verbose_name='Number of days left in subscription. Gets decreased daily by Django management command'
    )

    def __str__(self):
        return str(f'{self.subscription_type} id:{self.id.id}') 

    def __unicode__(self):
        return str(f'{self.subscription_type} id:{self.id.id}') 

    @property
    def get_owner(self):
        return self.owner.first()
    get_owner.fget.short_description = 'Owner'

