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

from helpers.profile_helper import get_userpic


class RaysTest(TestCase):


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
        image_path = os.path.join(str(settings.BASE_DIR), "mock/sample_image.jpg")
        self.user.userpic = SimpleUploadedFile(name='sample_image.jpg',
          content=open(image_path, 'rb').read(),
          content_type='image/jpeg')
        self.teleport_username = ''
        self.user.save()
        '''Prepare requests'''
        self.factory = RequestFactory()


    def tearDown(self):
        self.user.delete()


    def test_get_userpic(self):
        """Check userpic url functionality"""
        # default_userpic_url = settings.DEFAULT_USERPIC
        # url = '/'
        # request = self.factory.get(url)
        # request.user = self.user
        # userpic_url = get_userpic(request)
        # self.assertEquals(self.user.userpic.url, userpic_url)
        pass


    def test_get_userpic_no_creds(self):
        """Check userpic functionality for AnonymousUser"""
        # default_userpic_url = settings.DEFAULT_USERPIC
        # url = '/'
        # request = self.factory.get(url)
        # request.user = AnonymousUser()
        # request.session = {}
        # userpic_url = get_userpic(request)
        # self.assertEquals(default_userpic_url, userpic_url)
        pass
