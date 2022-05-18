import os
import datetime
import logging
import json

from django.conf import settings
from django.test import TestCase
from django.core.management import call_command
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from rays.models.ray_canned import RayCanned
from rays.models.ray import Ray
from rays.models.ray import Ray
from rays.routes_automation import *


class RoutesAutomationTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        self.RAY_SOURCES = settings.RAY_SOURCES
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


    def test_routes_create_no_creds(self):
        """Test creation of Routes template by an AnonymousUser"""

        url = '/'
        request = self.factory.post(url)
        request.user = AnonymousUser()
        request.session = {}
        response = create(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_routes_create(self):
        """Test creation of Routes canned Ray"""
        url = '/'
        """check empty request behavior"""
        request = self.factory.post(url, content_type='application/json')
        request.user = self.user_from
        response = create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty request')
        """Check partial data request behavior"""
        data = {
          'wrong_title': 'test title',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty title')
        """Check partial data request behavior"""
        data = {
          'title': 'test title',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty body')
        """Check full data request behavior"""
        data = {
          'title': 'test title',
          'body': 'test body',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = create(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['message'], 'canned message created')
        message = RayCanned.objects.all().last()
        self.assertEquals(message.body, 'test body')


    def test_routes_list_no_creds(self):
        """Test listing of Routes template by an AnonymousUser"""

        url = '/'
        request = self.factory.get(url)
        request.user = AnonymousUser()
        request.session = {}
        response = list_all(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_routes_list(self):
        """Test creation of Routes canned Ray"""
        url = '/'
        """check empty request behavior"""
        canned1 = RayCanned.objects.create(
          title='sample title1',
          slug='sample_slug1',
          body='sample body1'
        )
        canned2 = RayCanned.objects.create(
          title='sample title2',
          slug='sample_slug2',
          body='sample body2'
        )
        self.user_from.rays_canned.add(canned1)
        self.user_from.rays_canned.add(canned2)
        request = self.factory.get(url, content_type='application/json')
        request.user = self.user_from
        response = list_all(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)[0]['title'], 'sample title1')
        self.assertEquals(json.loads(response.content)[1]['title'], 'sample title2')


    def test_routes_show(self):
        """Test creation of Routes canned Ray"""
        url = '/'
        """check empty request behavior"""
        canned1 = RayCanned.objects.create(
          title='sample title1',
          slug='sample_slug1',
          body='sample body1'
        )
        canned2 = RayCanned.objects.create(
          title='sample title2',
          slug='sample_slug2',
          body='sample body2'
        )
        self.user_from.rays_canned.add(canned1)
        self.user_from.rays_canned.add(canned2)
        request = self.factory.get(url, content_type='application/json')
        request.user = self.user_from
        response = show(request, slug=canned2.slug)
        self.assertEquals(response.status_code, 200)


    def test_routes_reply(self):
        """Test creation of Routes canned Ray message"""
        url = '/'
        canned1 = RayCanned.objects.create(
          title='sample title1',
          slug='sample_slug1',
          body='sample body1'
        )
        self.user_from.rays_canned.add(canned1)
        """check wrong method behavior"""
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        
        request = self.factory.get(url)
        request.user = self.user_from
        response = create_message(request)
        logger.setLevel(previous_level)
        self.assertEquals(response.status_code, 405)
        """check POST behavior (message creation)
        for AnonymousUser
        """
        # check empty data
        data = {}
        request = self.factory.post(url, data, content_type='application/json')
        request.user = AnonymousUser()
        request.session = {}
        response = create_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty request')
        # check partial data
        data = {
          'id': canned1.id,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = AnonymousUser()
        request.session = {}
        response = create_message(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty message body')
        # check full correct data
        data = {
          'id': canned1.id,
          'message': 'test message body',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = AnonymousUser()
        request.session = {}
        response = create_message(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['message'], 'message sent')
        # check message is created
        # message = 
        # logging.info()
