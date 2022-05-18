import datetime
import logging
import json

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

import timer.views as timer
from moneta.models import BusinessEntity
from timer.models import WorkPeriod
from timer.models import UserInfo


class TimerTest(TestCase):

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
        '''create a default business entity to tie a timer to'''
        self.business_entity = BusinessEntity.objects.create(pk=0, name='Not set')

    def tearDown(self):
        # self.user_wrong.delete()
        self.user.delete()


    def test_timer_start_no_creds(self):
        """Make sure that unauthorised dude can't access timer start()"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = timer.tm_start(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_timer_start(self):
        """Check if we can start timer"""
        url = '/'
        """Start timer with no user_id present"""
        data = {}
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user
        response = timer.tm_start(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'no user id specified')
        """Start timer with user_id present"""
        data = {
          'user_id': self.user.id.id,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.POST = data
        request.user = self.user
        response = timer.tm_start(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_data['result'], 'Ok')
        self.assertEquals(response_data['message'], 'Timer started for user: ' + str(self.user.id.id))


    def test_timer_stop_no_creds(self):
        """Make sure that unauthorised dude can't access timer stop()"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = timer.tm_stop(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_timer_stop(self):
        """Check if we can stop timer"""
        url = '/'
        """Stop timer with no user_id present"""
        data = {}
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user
        response = timer.tm_stop(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'no user id specified')
        """Stop non-existant"""
        data = {
          'user_id': self.user.id.id,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.POST = data
        request.user = self.user
        response = timer.tm_stop(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 404)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'no such timer')

        """Create a timer that is already stopped"""
        stopped_timer = WorkPeriod(user_id=self.user.id)
        stopped_timer.timer_start = timezone.now() - datetime.timedelta(1)
        stopped_timer.timer_stop = timezone.now()
        days = stopped_timer.timer_stop.day-stopped_timer.timer_start.day
        hours = stopped_timer.timer_stop.hour-stopped_timer.timer_start.hour
        minutes = stopped_timer.timer_stop.minute-stopped_timer.timer_start.minute
        seconds = stopped_timer.timer_stop.second-stopped_timer.timer_start.second
        stopped_timer.duration = days*86400+hours*3600+minutes*60+seconds
        stopped_timer.save()
        """Try to stop timer that is stopeed already"""
        response = timer.tm_stop(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 204)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'timer stopped already')
        """Create an active timer"""
        active_timer = WorkPeriod(user_id=self.user.id)
        active_timer.timer_start = timezone.now() - datetime.timedelta(1)
        active_timer.timer_stop = None
        active_timer.save()
        response = timer.tm_stop(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_data['result'], 'Ok')
        self.assertEquals(response_data['message'], 'Timer stopped for user: ' + str(self.user.id.id))


    def test_get_timer(self):
        """Check if we can use get_timer functionality
        :todo: consider checking real data in JsonResponse for GET
        """

        url = '/'
        data = {}
        """call get_timer with GET request"""
        request = self.factory.get(url)
        request.user = self.user
        response = timer.get_timer(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'no user id specified')
        """call get_timer with GET request and user_id"""
        url = '/?user_id=' + str(self.user.id.id)
        request = self.factory.get(url)
        request.user = self.user
        response = timer.get_timer(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        """call get_timer with POST request, no ph, no rate"""
        data = {
          'user_id': self.user.id.id,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user
        request.POST = data
        response = timer.get_timer(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'no paid hours (ph) specified')
        """call get_timer with POST request, no rate"""
        data = {
          'user_id': self.user.id.id,
          'ph': 12,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user
        request.POST = data
        response = timer.get_timer(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(response_data['result'], 'error')
        self.assertEquals(response_data['message'], 'no rate specified')
        """create UserInfo object"""
        user_info_data = UserInfo(user_id=self.user.id)
        user_info_data.save()
        """call get_timer with POST request data all set"""
        data = {
          'user_id': self.user.id.id,
          'ph': 12,
          'rate': 2,
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user
        request.POST = data
        response = timer.get_timer(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_data['result'], 'Ok')
        self.assertEquals(response_data['message'], 'User info data saved successfully')
