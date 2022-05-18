from django.db import models
from django.contrib import admin

from djmoney.models.fields import MoneyField
from hashid_field import HashidAutoField

from accounts.models import User
from subscription.models import Payment


class Card(models.Model):
    """Stripe meta-data used for payment without having to type in card numbers
    saved for future use"""

    id = HashidAutoField(primary_key=True)
    owner = models.ManyToManyField(
        User, related_name='cards', blank=True,
        verbose_name='Person who can use the card (might be multiple)'
    )
    payment = models.ManyToManyField(
        Payment, related_name='cards', blank=True,
        verbose_name='Payment, made using the card'
    )
    brand = models.CharField(
        max_length=255, unique=False, default='',
        verbose_name='Card\'s brand, eg Visa, MasterCard etc'
    )
    payment_method_id = models.CharField(
        max_length=255, unique=False, default='',
        verbose_name='Card\'s payment_method id inside Stripe'
    )
    card_fingerprint = models.CharField(
        max_length=255, unique=False, default='fail',
        verbose_name='Stripe\'s hash for the Card'
    )
    last4 = models.CharField(
        max_length=4, unique=False, null=True, default=None,
        verbose_name='Last 4 digits of the card'
    )
    created_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name='Can this card be used for payments?'
    )

    def __str__(self):
        return str(self.id) 

    def __unicode__(self):
        return str(self.id) 
