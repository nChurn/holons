import datetime
import logging
import json
import os

from django.conf import settings
from django.test import TestCase
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from helpers.redirect_helper import perform_redirect
from helpers.slug_helper import view_by_slug
from rays.models.ray_canned import RayCanned


class RedirectHelperTest(TestCase):


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
          phone_number='123',
          handle='samplehandle',
          bio='sample bio'
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


    def test_perform_redirect_empty(self):
        """Check passthrough the redirector"""
        request = self.factory.get('/rays')
        request.user = AnonymousUser()
        request.session = {}
        response = perform_redirect(request)
        self.assertEquals(response.status_code, 302)


    def test_perform_redirect_by_slug(self):
        """Check passthrough the redirector"""
        request = self.factory.get('/samplehandle')
        request.user = self.user
        response = view_by_slug(request, 'samplehandle')
        self.assertEquals(response.status_code, 200)
        request = self.factory.get('/profile-slug')
        request.user = self.user
        canned1 = RayCanned.objects.create(
          title='sample title1',
          slug='sample_slug1',
          body='sample body1'
        )
        self.user.rays_canned.add(canned1)
        response = view_by_slug(request, canned1.slug)
        self.assertEquals(response.status_code, 200)
