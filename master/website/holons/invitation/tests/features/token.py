import json
import datetime
import logging
import pprint

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from invitation.token import smart_redirect
from invitation.token import token_change_status
from helpers.token_helper import token_generate
from invitation.models import Token
from invitation.views import generate_layers_invite


class InvitationTokenTest(TestCase):

    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        """Create a new user"""

        date_stamp = self.date_stamp
        self.password = '22test22'
        self.username = 'test_' + date_stamp
        self.user = get_user_model().objects.create_user(
          username=self.username,
          password=self.password,
          email=self.username + '@holons-test.me',
          phone_number='123'
        )
        self.user.save()
        '''Prepare requests'''
        self.factory = RequestFactory()
        '''Prepare tokens of all known types'''
        self.token_str = token_generate(delimiter='-')
        self.token = Token.objects.create(
          value=self.token_str,
          token_type='generic',
          status='created'
        )
        self.token_str_invitation = token_generate(delimiter='-')
        self.token_invitation = Token.objects.create(
          value=self.token_str_invitation,
          token_type='invitation',
          status='created'
        )
        self.token_str_offer = token_generate(delimiter='-')
        self.token_offer = Token.objects.create(
          value=self.token_str_offer,
          token_type='offer',
          status='created'
        )
        self.token_str_layers = token_generate(delimiter='-')
        self.token_layers = Token.objects.create(
          value=self.token_str_layers,
          token_type='layers',
          status='created'
        )

    def tearDown(self):
        self.user.delete()

    def test_smart_redirect_no_token(self):
        """Prepare a request object for a redirect"""
        request = self.factory.post('/agenda')
        request.user = self.user
        redirected_response = smart_redirect(request, token='', delete_token_cookie=False)
        """Ensure we are redirected"""
        self.assertEquals(redirected_response.status_code, 302)

    def test_smart_redirect_no_token_delete_cookie(self):
        """Prepare a request object for a redirect"""
        request = self.factory.post('/agenda')
        request.user = self.user
        redirected_response = smart_redirect(request, token='', delete_token_cookie=True)
        """Ensure we are redirected"""
        self.assertEquals(redirected_response.status_code, 302)
        
    def test_smart_redirect_token_set_leave_cookie_be(self):
        """Prepare a request object for a redirect"""
        request = self.factory.post('/agenda')
        request.user = self.user
        redirected_response = smart_redirect(request, token=self.token_str, delete_token_cookie=False)
        """Ensure we are redirected"""
        self.assertEquals(redirected_response.status_code, 302)

    def test_smart_redirect_invitation_token(self):
        """Ensure we are redirected to the token-specific offer URL"""
        request = self.factory.post('/agenda')
        request.user = self.user
        redirected_response = smart_redirect(request, token=self.token_str_invitation)
        self.assertEquals(redirected_response.status_code, 302)
        self.assertEquals(redirected_response.url, '/auth?token=' + self.token_str_invitation)

    def test_smart_redirect_offers_token(self):
        """Ensure we are redirected to the token-specific offer URL"""
        request = self.factory.post('/agenda')
        request.user = self.user
        redirected_response = smart_redirect(request, token=self.token_str_offer)
        self.assertEquals(redirected_response.status_code, 302)
        self.assertEquals(redirected_response.url, '/relations/offers/' + self.token_str_offer)

    def test_smart_redirect_layers_token(self):
        """Ensure we are redirected to the token-specific offer URL"""
        url = '/auth?token=123-example-token&redirect_to=layers&project=555'
        request = self.factory.post(url)
        request.user = self.user
        redirected_response = smart_redirect(request, token=self.token_str_layers)
        self.assertEquals(redirected_response.status_code, 302)
        # self.assertEquals(redirected_response.url, '/layers?token=' + self.token_str_layers)

    def test_layers_invite(self):
        """Ensure we are saving Taiga-generated token correctly"""
        token_str = 'test-taiga-invite-token-213'
        request = self.factory.post(
                                    '/invitation/generate-layers-invite',
                                    data = json.dumps({'token': token_str}),
                                    content_type='application/json')
        request.user = self.user
        token_response = json.loads(generate_layers_invite(request).content)['data']['code']
        check_token = Token.objects.filter(value=token_str).first()
        self.assertEquals(token_response, check_token.value)
        self.assertEquals(check_token.token_type, 'layers')


    def test_token_change_status(self):
        """Check token status changes"""
        ''' existing token '''
        token_change_success = token_change_status(self.token_str)
        self.assertEquals(token_change_success, True)
        ''' wrong token '''
        token_change_success = token_change_status(self.token_str + '_nonexist')
        self.assertEquals(token_change_success, False)
