import datetime
import logging
import json

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from helpers.render_helper import custom_render


class CustomRenderTest(TestCase):


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
        self.user.delete()


    def test_custom_render_redirect_to(self):
        """Check custom render redirect_to functionality"""
        redirect_url = 'email'
        request = self.factory.get('/rays?redirect_to=' + redirect_url)
        request.user = self.user
        response = custom_render(request, 'rays')
        self.assertEquals(response.status_code, 302)


    def test_custom_render_layers(self):
        """Check custom render redirect_to functionality
        :todo: Fix smart_redirect/custom render functionality, then test
        """
        redirect_url = 'layers'
        invite_str = 'nonexistant invite'
        request = self.factory.get('?invite=' + invite_str)
        request.user = AnonymousUser()
        request.session = {}
        # response = custom_render(request, 'layers.html')
        pass
        # self.assertEquals(response.status_code, 200)
