import os
import datetime
import logging
import json

from django.conf import settings
from django.test import TestCase
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from email_api.helpers import auth_helper
from email_api.helpers import request_helper


class EmailApiHelpersTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        date_stamp = self.date_stamp
        self.password = '12test12'
        self.username = 'test_' + date_stamp

        self.username_second = 'test_wrong' + date_stamp
        self.user_from = get_user_model().objects.create_user(
          username=self.username + '_from',
          password=self.password,
          email=self.username + '_from' + '@holons-test.me',
          phone_number='123'
        )
        self.user_to = get_user_model().objects.create_user(
          username=self.username + '_to',
          password=self.password,
          email=self.username  + '_to' + '@holons-test.me',
          phone_number='222'
        )
        self.user_third = get_user_model().objects.create_user(
          username=self.username + '_third',
          password=self.password,
          email=self.username  + '_third' + '@holons-test.me',
          phone_number='333'
        )
        image_path = os.path.join(str(settings.BASE_DIR), "mock/sample_image.jpg")
        self.user_from.userpic = SimpleUploadedFile(name='sample_image.jpg',
          content=open(image_path, 'rb').read(),
          content_type='image/jpeg')
        self.teleport_username = ''
        self.user_from.save()
        self.user_to.save()
        '''Prepare requests'''
        self.factory = RequestFactory()

        self.message1 = {
          'subject': 'message1 subject',
          'message_body': 'message1 body',
        }
        self.message2 = {
          'subject': 'message2 subject',
          'message_body': 'message2 body',
        }
        self.message3 = {
          'subject': 'message3 subject',
          'message_body': 'message3 body',
        }


    def tearDown(self):
        self.user_from.delete()
        self.user_to.delete()


    def test_get_user_no_creds(self):
        """Test a helper with AnonymousUser"""
        url = '/'
        request = self.factory.post(url)
        request.user = AnonymousUser()
        request.session = {}
        user = auth_helper.get_user(request)
        self.assertEquals(str(user), 'AnonymousUser')


    def test_get_user(self):
        """Test getting a user username"""
        url = '/'
        request = self.factory.post(url)
        request.user = self.user_from
        user = auth_helper.get_user(request)
        self.assertEquals(user.id, self.user_from.id)


    def test_method_helper(self):
        """Test getting a user username"""
        url = '/'
        request = self.factory.get(url)
        request.user = self.user_from
        method = request_helper.method_name(request)
        self.assertEquals(method, 'get')
        request = self.factory.post(url)
        request.user = self.user_from
        method = request_helper.method_name(request)
        self.assertEquals(method, 'post')
        request = self.factory.delete(url)
        request.user = self.user_from
        method = request_helper.method_name(request)
        self.assertEquals(method, 'delete')
        request = self.factory.patch(url)
        request.user = self.user_from
        method = request_helper.method_name(request)
        self.assertEquals(method, 'patch')
        request = self.factory.put(url)
        request.user = self.user_from
        method = request_helper.method_name(request)
        self.assertEquals(method, 'put')


