import json
import datetime
import logging

from django.test import TestCase
from django.test import RequestFactory
from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.urls import reverse

from holons.urls import urlpatterns
from holons import views


class HolonsViewsTest(TestCase):
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
        self.user.cors_storage = json.dumps({'test': 'test'})
        self.user.save()
        '''Prepare requests'''
        self.factory = RequestFactory()


    def tearDown(self):
        self.user.delete()


    def test_200_url(self, url='/'):
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        try:
          response = self.client.get(url, follow=True)
        except Http404: 
          pass
        logger.setLevel(previous_level)
        '''Ensure we get 200'''
        self.assertEquals(response.status_code, 200)


    def test_404_url(self, url='/nonexistent-url-123'):
        logger = logging.getLogger('django.request')
        previous_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        try:
          response = self.client.get(url, follow=True)
        except Http404: 
          pass
        logger.setLevel(previous_level)
        '''Ensure we get 404'''
        self.assertEquals(response.status_code, 404)


    def test_responses(self):
       """Go over main URLs file and check if they're available"""
       for url in urlpatterns:
          try:
            if url.name not in ('index', 'login', 'logout',
              'classic_login', 'cors_data', 'render_offer',
              'profile_public_handle', 'profile_public', 
              'view_by_slug', 'impersonate'):
              if 'api' not in url.name\
                and 'subscribe' not in url.name\
                and 'relations' not in url.name\
                and 'offers' not in url.name:
                # logging.info(url.name)
                # logging.info(' ')
                # :todo: check each excluded url separately
                # :todo: test all API features
                response = self.client.get(reverse(url.name))
                self.assertEqual(response.status_code, 200)
          except AttributeError:
            # logging.info(url)
            # check dynamic urls in separate tests
            pass
            

    def test_login_url(self):
        """First check login url as anonymous user"""
        response = self.client.get('/login', follow=True)
        '''Ensure we get 200'''
        self.assertEquals(response.status_code, 200)
        '''Login a user, and call login view'''
        request_logged_in = self.factory.post('/')
        user = authenticate(username=self.username, password=self.password)
        request_logged_in.user = user
        response_logged_in = views.login(request_logged_in)
        '''Check if we are redirected'''
        self.assertEquals(response_logged_in.status_code, 302)
        '''Check if the redirect page exists'''
        self.test_200_url(url=response_logged_in.url)


    def test_classic_login_url(self):
        response = self.client.get('/classic-login', follow=True)
        '''Ensure we get 200'''
        self.assertEquals(response.status_code, 200)


    def test_logout_url(self):
        request = self.factory.get('/logout')
        user = authenticate(username=self.username, password=self.password)
        request.user =user
        request.session = self.client.session
        response = views.logout_user(request)
        '''Ensure we get redirected'''
        self.assertEquals(response.status_code, 302)

    
    def test_layers_hosting_url(self):
        response = self.client.get('/layers/hosting', follow=True)
        '''Ensure we get 200'''
        self.assertEquals(response.status_code, 200)


    def test_404_handler(self):
        request = self.factory.post('/')
        response = views.handler404(request)
        '''Check if we are getting 404'''
        self.assertEquals(response.status_code, 404)


    def test_500_handler(self):
        request = self.factory.post('/')
        response = views.handler500(request)
        '''Check if we are getting 500'''
        self.assertEquals(response.status_code, 500)


    def test_cors_data(self):
        request = self.factory.post('/')
        user = authenticate(username=self.username, password=self.password)
        request.user = user
        response = views.cors_data(request)
        '''Check if we are getting 200'''
        self.assertEquals(response.status_code, 200)

