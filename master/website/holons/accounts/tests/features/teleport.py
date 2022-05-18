from django.test import TestCase
import datetime
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from accounts.views import teleport_user_not_exists
from accounts.views import teleport_user_register

import logging

class TeleportUserExistsTest(TestCase):

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

    def tearDown(self):
        # self.user_wrong.delete()
        self.user.delete()

    def test_django_user_login(self):
        """ login to Django """
        user = authenticate(username=self.username, password=self.password)
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_teleport_user_register(self):
        """ register a new user in teleport
        :todo: Mock teleport API calls instead of calling the server each time
        """
        user = self.user
        self.assertNotEqual(
          None,
          teleport_user_register(user).get('access_token', None)
        )

    def test_teleport_correct_user_exists(self):
        """ check for nonexistant username in teleport
        :todo: Mock teleport API calls instead of calling the server each time
        """
        user = self.user
        user.username = user.username + '_wrong'
        self.assertTrue(teleport_user_not_exists(user))

    def test_teleport_wrong_user_not_exists(self):
        """ check if username is available in teleport
        :todo: Mock teleport API calls instead of calling the server each time
        """
        user = self.user
        self.assertFalse(teleport_user_not_exists(user))

