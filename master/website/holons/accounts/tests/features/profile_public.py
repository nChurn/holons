import datetime
import logging
import json

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from accounts import profile
from accounts.models import User


class ProfilePublicTest(TestCase):


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


    def test_user_profile_no_creds(self):
        pass


    def test_user_profile(self):
        pass
