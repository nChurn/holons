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


class ProfileTest(TestCase):


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


    def test_edit_no_creds(self):
        """Check if unauthorised dude can't edit user profile"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = profile.edit(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_edit(self):
        """Check if we can edit user profile"""
        data = json.dumps({})
        request = self.factory.post('/')
        request._body = data
        request.user = self.user
        response = profile.edit(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)


    def test_change_username(self):
        """Set a new username"""
        data = json.dumps({'username': 'Changed Username'})
        request = self.factory.post('/')
        request._body = data
        request.user = self.user
        response = profile.edit(request)
        check_user = User.objects.filter(pk=self.user.id).first()
        self.assertEquals(check_user.username, 'Changed Username')


    def test_change_handle(self):
        """Set a new handle"""
        data = json.dumps({'handle': 'Changed handle'})
        request = self.factory.post('/')
        request._body = data
        request.user = self.user
        response = profile.edit(request)
        check_user = User.objects.filter(pk=self.user.id).first()
        self.assertEquals(check_user.handle, 'Changed handle')


    def test_change_bio(self):
        """Set a new bio"""
        data = json.dumps({'bio': 'Changed bio'})
        request = self.factory.post('/')
        request._body = data
        request.user = self.user
        response = profile.edit(request)
        check_user = User.objects.filter(pk=self.user.id).first()
        self.assertEquals(check_user.bio, 'Changed bio')


    def test_image_upload_no_creds(self):
        """Make sure that unauthorised dude can't upload userpic"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = profile.picture_upload(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')
