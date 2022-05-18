import pytz
import datetime
import logging
import json

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from health.status import rays as rays_health
from health.models import TalentStat


class HealthTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        date_stamp = self.date_stamp
        self.password = '12test12'
        self.username = 'test_' + date_stamp
        self.username_wrong = 'test_wrong' + date_stamp
        self.user = get_user_model().objects.create_user(
          username=self.username,
          password=self.password,
          email=self.username + '@holons-test.me',
          phone_number='123'
        )
        self.teleport_username = ''
        self.user.save()
        '''Prepare requests'''
        self.factory = RequestFactory()


    def tearDown(self):
        # self.user_wrong.delete()
        self.user.delete()


    def test_status(self):
        """Check empty stats"""
        stats = rays_health()
        self.assertEquals(len(stats), 23)
        """Create a stat record"""
        check_date = timezone.now() - datetime.timedelta(days=1)
        stat_record = TalentStat.objects.create(check_date=check_date)
        check_date = timezone.now() - datetime.timedelta(days=2)
        stat_record = TalentStat.objects.create(check_date=check_date)
        check_date = timezone.now() - datetime.timedelta(days=3)
        stat_record = TalentStat.objects.create(check_date=check_date)

        now = timezone.now()
        monday = now + datetime.timedelta(days=-now.weekday())
        monday = monday.replace(hour=00, minute=00, second=1)
        week_logs = TalentStat.objects.filter(check_date__range=[monday, now])
        stats = rays_health()

        self.assertEquals(len(stats), 23)


