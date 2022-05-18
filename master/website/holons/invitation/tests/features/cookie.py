import json
import logging
import datetime

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from holons.views import index
from invitation.views import invitation_generate_code
from helpers.token_helper import token_generate
from invitation.cookie import set_invitation_cookie
from invitation.cookie import get_invitation_cookie
from invitation.cookie import delete_invitation_cookie
from invitation.models import Token


class InvitationUserExistsTest(TestCase):

    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        """
        Create a new user
        """

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
        self.factory = RequestFactory()

    def tearDown(self):
        self.user.delete()


    def test_invitation_token_generation(self):
        """ make a request to the invitation code generator """
        request = self.factory.post('/invitation/get-code')
        request.user = self.user
        response = invitation_generate_code(request)
        """ ensure url is not dead """
        self.assertEqual(response.status_code, 200)
        """ ensure data.code is a string """
        self.assertEqual(type(json.loads(response.content)['data']['code']), str)
        """ ensure invitation code is of a certain length """
        self.assertEqual(len(json.loads(response.content)['data']['code']), 27)
        

    def test_set_invitation_cookie(self):
        """
        * generate token,
        * add it to the DB,
        * send it to the cookie,
        * check if token in cookie equals generated token string
        """

        token_str = token_generate(delimiter='-')
        token = Token.objects.create(
          value=token_str,
          token_type='invitation',
          status='created'
        )
        token.issuer.add(self.user.id)
        token.save()
        """ set cookie """
        response = self.client.get('/?token=' + token_str, follow=True)
        token_check = (dict(response.client.cookies.items()).get('holons_invitation', None)).value
        """ ensure url is not dead """
        self.assertEqual(response.status_code, 200)
        """ ensure token from cookie == token generated """
        self.assertEqual(token_check, token_str)


    def test_get_invitation_cookie_empty(self):
        """
        * generate token,
        * add it to the DB,
        * send it to the cookie,
        * check if token in cookie is empty using helper method
        """

        token_str = token_generate(delimiter='-')
        token = Token.objects.create(
          value=token_str,
          token_type='invitation',
          status='created'
        )
        token.issuer.add(self.user.id)
        token.save()
        """ set cookie """
        response = self.client.get('/?token=' + token_str, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        token_check = get_invitation_cookie(request)
        """ ensure token from cookie == token generated """
        self.assertEqual(token_check, '')


    def test_get_invitation_cookie(self):
        """
        * generate token,
        * add it to the DB,
        * send it to the cookie,
        * check if token in cookie equals token string using helper method
        """
        
        token_str = token_generate(delimiter='-')
        token = Token.objects.create(
          value=token_str,
          token_type='invitation',
          status='created'
        )
        token.issuer.add(self.user.id)
        token.save()
        """ set cookie """
        response = self.client.get('/?token=' + token_str, follow=True)
        request = self.factory.get('/')
        request.user = self.user
        """ transfer cookie to the test request """
        request.COOKIES['holons_invitation'] = (dict(response.client.cookies.items()).get('holons_invitation', None)).value
        token_check = get_invitation_cookie(request)
        """ ensure token from cookie == token generated """
        self.assertEqual(token_check, token_str)


    def test_delete_invitation_cookie(self):
        """
          * generate token,
          * add it to the DB,
          * send it to the cookie,
          * check if we can delete the cookie using helper method
          :todo: seems we are doing it wrong (checking for empty string instead of the cookie itself)
        """

        token_str = token_generate(delimiter='-')
        token = Token.objects.create(
          value=token_str,
          token_type='invitation',
          status='created'
        )
        token.issuer.add(self.user.id)
        token.save()
        ''' set cookie '''
        response = self.client.get('/?token=' + token_str, follow=True)
        ''' ensure url is not dead '''
        self.assertEqual(response.status_code, 200)
        no_cookie_response = delete_invitation_cookie(response)
        token_check = dict(no_cookie_response.client.cookies.items()).get('holons_invitation', None).value
        self.assertEqual(token_check, '')
