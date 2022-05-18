import datetime
import json
import logging
import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import RequestFactory
from django.test import TestCase

from moneta.business_entities import *
from moneta.models import BusinessEntity


class BusinessEntityTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        self.RAY_SOURCES = settings.RAY_SOURCES
        image_path = os.path.join(str(settings.BASE_DIR), "mock/sample_image.jpg")
        userpic = SimpleUploadedFile(name='sample_image.jpg',
          content=open(image_path, 'rb').read(),
          content_type='image/jpeg')
        call_command('loaddata', 'accounts/seed/fixed_users.json', verbosity=0)
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
        self.user_from.userpic = userpic
        self.user_to = get_user_model().objects.create_user(
          username=self.username + '_to',
          password=self.password,
          email=self.username  + '_to' + '@holons-test.me',
          phone_number='222'
        )
        self.user_to.userpic = userpic
        self.user_third = get_user_model().objects.create_user(
          username=self.username + '_third',
          password=self.password,
          email=self.username  + '_third' + '@holons-test.me',
          phone_number='333'
        )
        self.user_third.userpic = userpic
        self.teleport_username = ''
        self.user_from.save()
        self.user_to.save()
        self.user_third.save()
        '''Prepare requests'''

        self.factory = RequestFactory()


    def tearDown(self):
        self.user_from.delete()
        self.user_to.delete()
        self.user_third.delete()


    def test_business_entity_creation(self):
        """test sending a direct message"""
        url = '/'
        return
        """check empty request behavior"""
        request = self.factory.post(url, content_type='application/json')
        request.user = self.user_from
        response = rays_custom_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty request')
