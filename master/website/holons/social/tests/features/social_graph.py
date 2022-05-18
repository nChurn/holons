import json
import datetime
import logging

from django.test import TestCase
from django.core.management import call_command
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

from helpers.token_helper import token_generate
from invitation.models import Token
from social.views import update_social_graph
from social.views import address_book
from social.views import get_address_book


class SocialGraphTest(TestCase):
    

    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        call_command('loaddata', 'accounts/seed/fixed_users.json', verbosity=0)
        """Create a new user"""

        date_stamp = self.date_stamp
        ''' invite-giver user '''
        self.password = '22test22'
        self.username = 'test_' + date_stamp
        self.user = get_user_model().objects.create_user(
          username=self.username,
          password=self.password,
          email=self.username + '@holons-test.me',
          phone_number='123'
        )
        self.user.save()
        ''' invite-taker user '''
        self.child_user = get_user_model().objects.create_user(
          username=self.username + '_child',
          password=self.password,
          email=self.username + '_child@holons-test.me',
          phone_number='222'
        )
        self.child_user.save()
        '''Prepare requests'''
        self.factory = RequestFactory()
        '''Prepare tokens of all known types'''
        self.token_str = token_generate(delimiter='-')
        self.token = Token.objects.create(
          value=self.token_str,
          token_type='generic',
          status='created'
        )
        self.token.issuer.add(self.user)
        self.token.used_by.add(self.child_user)


    def tearDown(self):
        self.user.delete()
        self.child_user.delete()


    def test_address_book_no_creds(self):
        """Make sure that unauthorised dude can't get address_book"""
        request = self.factory.get('/')
        request.user = AnonymousUser()
        request.session = {}
        response = address_book(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_address_book(self):
        """Update social graph"""
        update_social_graph(self.token)
        request = self.factory.get('/')
        request.user = self.user
        response = address_book(request)
        """Make sure that user can get address_book"""
        self.assertEquals(response.status_code, 200)
        """Make sure self.user has address book,
        containing self.child_user in it """
        user_id = json.loads(response.content)['contacts'][0]['user_id']
        self.assertEquals(self.child_user.id, user_id)
        request = self.factory.get('/')
        """Make one more request and make sure self.child_user has address book,
        containing self.user in it """
        request.user = self.child_user
        request.session = {}
        response = address_book(request)
        user_id = json.loads(response.content)['contacts'][0]['user_id']
        self.assertEquals(self.user.id, user_id)

