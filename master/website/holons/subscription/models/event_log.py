from django.db import models
from django.contrib import admin

from djmoney.models.fields import MoneyField
from hashid_field import HashidAutoField
from django_jsonfield_backport.models import JSONField

from accounts.models import User


class EventLog(models.Model):
    """
    Used to provide idempotency for payment-related webhook events
    """

    event_id =  models.CharField(max_length=255, unique=False, default='')
    event_type = models.CharField(max_length=255, unique=False, default='')
    event_data = JSONField(default=None, null=True)
    created_at = models.DateTimeField(auto_now=True,
                                      blank=True, null=True)
    def __str__(self):
        return str(self.event_id) 

    def __unicode__(self):
        return str(self.event_id) 
