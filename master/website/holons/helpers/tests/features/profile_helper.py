import datetime
import json
import logging
import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory
from django.test import TestCase

from helpers.profile_helper import get_account_status
from helpers.profile_helper import get_bio
from helpers.profile_helper import get_handle
from helpers.profile_helper import get_username
from helpers.profile_helper import get_userpic
from helpers.profile_helper import impersonate_accounts
from helpers.profile_helper import impersonate_menu_enabled


class ProfileHelperTest(TestCase):


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


    def test_get_account_status(self):
        """Check account_status functionality"""
        url = '/'
        account_status = 'core'
        self.user.account_status = account_status
        self.user.save()
        request = self.factory.get(url)
        request.user = self.user
        user_account_status = get_account_status(request)
        self.assertEquals(account_status, user_account_status)


    def test_get_bio(self):
        """Check bio functionality"""
        url = '/'
        account_bio = 'sample account bio'
        self.user.bio = account_bio
        self.user.save()
        request = self.factory.get(url)
        request.user = self.user
        user_account_bio = get_bio(request)
        self.assertEquals(account_bio, user_account_bio)


    def test_get_handle(self):
        """Check handle functionality"""
        url = '/'
        account_handle = 'handleSample'
        self.user.handle = account_handle
        self.user.save()
        request = self.factory.get(url)
        request.user = self.user
        user_account_handle = get_handle(request)
        self.assertEquals(account_handle, user_account_handle)


    def test_get_username(self):
        """Check username functionality"""
        url = '/'
        username = 'sample username'
        self.user.username = username
        self.user.save()
        request = self.factory.get(url)
        request.user = self.user
        user_account_username = get_username(request)
        self.assertEquals(username, user_account_username)


    def test_get_userpic(self):
        """Check userpic url functionality"""
        default_userpic_url = settings.DEFAULT_USERPIC
        url = '/'
        request = self.factory.get(url)
        request.user = self.user
        userpic_url = get_userpic(request)
        self.assertEquals(self.user.userpic.url, userpic_url)


    def test_get_impersonate_accounts(self):
        """Check if user is listed in the impersonate menu"""
        return
        url = '/'
        account_status = 'core'
        self.user.account_status = account_status
        self.user.save()
        request = self.factory.get(url)
        request.user = self.user
        user_account_status = get_account_status(request)
        self.assertEquals(account_status, user_account_status)


    def test_get_impersonate_menu_enabled(self):
        """Check impersonate menu availability functionality"""
        return
        url = '/'
        account_status = 'core'
        self.user.account_status = account_status
        self.user.save()
        request = self.factory.get(url)
        request.user = self.user
        user_account_status = get_account_status(request)
        self.assertEquals(account_status, user_account_status)
