import datetime
import logging

from django.test import TestCase
from django.contrib.auth import get_user_model

from timer.models import WorkPeriod
from timer.models import UserInfo
from moneta.models  import BusinessEntity

import logging

class TimerModelTest(TestCase):

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
        '''create a default business entity to tie a timer to'''
        self.business_entity = BusinessEntity.objects.create(pk=0, name='Not set')


    def tearDown(self):
        # self.user_wrong.delete()
        self.user.delete()

    """
    Test model fields
    """
    def test_work_period_model_str(self):
        w_period = WorkPeriod.objects.create(
          user_id=1,
          duration=20
        )
        self.assertEqual(str(w_period), str(20))
        

    def test_user_info_model_str(self):
        u_info = UserInfo.objects.create(
          user_id=1,
          rate=15
        )
        self.assertEqual(str(u_info), str(15))

