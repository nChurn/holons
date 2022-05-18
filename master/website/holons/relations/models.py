from django.db import models
from djmoney.models.fields import MoneyField

from django_jsonfield_backport.models import JSONField
from hashid_field import HashidAutoField

from accounts.models import User


class Offer(models.Model):
    id = HashidAutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=False, default='')
    from_name = models.CharField(max_length=255, unique=False, default='')
    to_name = models.CharField(max_length=255, unique=False, default='')
    terms_from = models.TextField(default='')
    terms_to = models.TextField(default='')
    consideration = models.TextField(default='')
    timeframe = models.TextField(default='')
    owner = models.ManyToManyField(User, related_name='offers', blank=True)
    accepted_by = models.ManyToManyField(User,
                                        related_name='offers_accepted', blank=True)
    invite_token = models.CharField(max_length=255, unique=False, default='')
    status = models.CharField(max_length=255)
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    paragraphs = JSONField(default=None, null=True)
    deadline_at = models.DateTimeField(auto_now=False,
                                      blank=True, null=True, default=None)
    hourly_rate = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                            blank=True, null=True, default=None)
    budget = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                            blank=True, null=True, default=None)
    currency = models.CharField(max_length=3, unique=False, default='USD')
    contract_type = models.CharField(max_length=255, default='')
    is_membership_sponsor = models.BooleanField(default=False)

    def __str__(self):
        return self.from_name + ' -> ' + self.to_name 

    def __unicode__(self):
        return self.from_name + ' -> ' + self.to_name 


class Invoice(models.Model):
    id = HashidAutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=False, default='')
    from_name = models.CharField(max_length=255, unique=False, default='')
    to_name = models.CharField(max_length=255, unique=False, default='')
    owner = models.ManyToManyField(User, related_name='invoices', blank=True)
    offer = models.ManyToManyField(Offer,
                                        related_name='invoices', blank=True)
    # :todo: rename accepted_by -> paid_by, or something
    accepted_by = models.ManyToManyField(User,
                                        related_name='invoices_accepted', blank=True)
    status = models.CharField(max_length=255)
    is_paid = models.BooleanField(default=False)
    due_date_at = models.DateTimeField(auto_now=False,
                                      blank=True, null=True, default=None)
    paid_at = models.DateTimeField(auto_now=False,
                                      blank=True, null=True, default=None)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency='USD',
                            blank=True, null=True, default=None)
    currency = models.CharField(max_length=3, unique=False, default='USD')

    def __str__(self):
        return self.from_name + ' -> ' + self.to_name 

    def __unicode__(self):
        return self.from_name + ' -> ' + self.to_name 
