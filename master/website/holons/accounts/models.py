import logging
from datetime import datetime, timezone, timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
from hashid_field import HashidAutoField

from email_api.models import Mailbox
from rays.models.direct_message import DirectMessage
from rays.models.ray import Ray
from rays.models.ray_canned import RayCanned
from rays.models.ray_source import RaySource
from rays.models.ray_template import RayTemplate
from rays.models.upwork_talent import UpworkTalent


class User(AbstractUser):
    """
    User model

    """
    USERPIC_UPLOAD_DIR = settings.USERPIC_UPLOAD_DIR
    DEFAULT_USERPIC = settings.DEFAULT_USERPIC

    
    id = HashidAutoField(primary_key=True, allow_int_lookup=True)
    username = models.CharField(max_length=255, unique=True, default='')
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=False, default='')
    handle = models.CharField(max_length=255, unique=False, default='')
    company_name = models.CharField(max_length=255, unique=False, default='')
    phone_number = models.CharField(max_length=128, unique=True, default='')
    token = models.CharField(default='', max_length=255)
    phone_confirmation_code = models.CharField(default='', max_length=255)
    phone_confirmed = models.BooleanField(default=False)
    userpic = models.ImageField(null=True,
                                upload_to=USERPIC_UPLOAD_DIR, default=DEFAULT_USERPIC)
    account_status = models.CharField(max_length=255, unique=False,
                                      default=settings.ACCOUNT_STATUSES[0][0])
    mailboxes = models.ManyToManyField(Mailbox, related_name='users', blank=True)
    rays = models.ManyToManyField(RaySource, related_name='users', blank=True)
    rays_canned = models.ManyToManyField(RayCanned, related_name='users', blank=True)
    ray_messages = models.ManyToManyField(
      UpworkTalent,
      related_name='users', blank=True
    )
    rays_direct = models.ManyToManyField(
      Ray, related_name='users', blank=True
    )
    rays_dm_recieved = models.ManyToManyField(
      DirectMessage,
      related_name='user_to', blank=True
    )
    rays_dm_sent = models.ManyToManyField(
      DirectMessage,
      related_name='user_from', blank=True
    )
    cors_storage = models.TextField(unique=False, default='')
    bio = models.CharField(max_length=512, unique=False, default='')
    is_profile_approved = models.BooleanField(default=False)
    country = models.CharField(default='', max_length=255)

    REQUIRED_FIELDS = []


    @property
    def platos_bids(self):
        bids_count = 0
        for campaign in self.campaigns.all():
            for campaign_template in campaign.templates.all():
                bids_count += campaign_template.bids_total
        return bids_count

    @property
    def platos_bids_this_week(self):
        """:TODO: Rewrite this using model relations user.campaigns.templates.log
        """
        from campaigns.models import Log as CampaignLog
        bids_count = 0
        template_ids = []
        now = datetime.now(timezone.utc)
        start_time = now - timedelta(seconds=60*60*24*7)  # week in seconds
        for campaign in self.campaigns.all():
            for campaign_template in campaign.templates.all():
                template_ids.append(campaign_template.pk)
        bids_count = CampaignLog.objects.filter(template_id__in=template_ids)\
                  .filter(event_date__range=[start_time, now])\
                  .filter(event_type='bid')\
                  .count()
        return bids_count

    @property
    def platos_replies_this_week(self):
        """:TODO: Rewrite this using model relations user.campaigns.templates.log
        """
        from campaigns.models import Log as CampaignLog
        replies_count = 0
        template_ids = []
        now = datetime.now(timezone.utc)
        start_time = now - timedelta(seconds=60*60*24*7)  # week in seconds
        for campaign in self.campaigns.all():
            for campaign_template in campaign.templates.all():
                template_ids.append(campaign_template.pk)
        replies_count = CampaignLog.objects.filter(template_id__in=template_ids)\
                  .filter(event_date__range=[start_time, now])\
                  .filter(event_type='reply')\
                  .count()
        return replies_count

    @property
    def platos_account_is_paid(self):
        if self.subscriptions\
                  .filter(subscription_type='platos full')\
                  .count() > 0:
            return True
        return False

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return f'id: {self.id.id} phone: {self.phone_number} {self.username}'

    def __unicode__(self):
        return f'id: {self.id.id} phone: {self.phone_number} {self.username}'
