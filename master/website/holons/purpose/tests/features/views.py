import datetime
import logging
import json

from django.test import TestCase
from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser

from accounts.models import User
from purpose.models import Item
import purpose.views as purpose



class PurposeTest(TestCase):


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


    def test_index_no_creds(self):
        """Check if unauthorised dude can't access index"""
        request = self.factory.get('/')
        request.user = AnonymousUser()
        request.session = {}
        response = purpose.index(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_index(self):
        """Check if we can access index"""
        data = json.dumps({})
        request = self.factory.get('/')
        item1 = Item.objects.create(title='Sample item1', value='Item value 1')
        item2 = Item.objects.create(title='Sample item2', value='Item value 2')
        self.user.purpose.add(item1)
        self.user.purpose.add(item2)
        request.user = self.user
        response = purpose.index(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response_data['data']['items'][0]['title'], 'Sample item1')


    def test_create_no_creds(self):
        """Check if unauthorised dude can't create items"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = purpose.create(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_create(self):
        """Check if we can create items"""
        """Check no data"""
        data = json.dumps({
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.create(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        data = json.dumps({
          'title': 'Sample item check CREATION',
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.create(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        data = json.dumps({
          'title': 'Sample item check CREATION',
          'value': 'Item value1'
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.create(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.user.purpose.first().title, 'Sample item check CREATION')


    def test_rename_no_creds(self):
        """Check if unauthorised dude can't create items"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = purpose.rename(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_rename(self):
        """Check if we can create items"""
        """Check no data"""
        data = json.dumps({})
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.rename(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        data = json.dumps({
          'item_id': 11,
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.rename(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        item1 = Item.objects.create(title='Sample item1', value='Item value 1')
        self.user.purpose.add(item1)
        data = json.dumps({
          'item_id': self.user.purpose.first().id,
          'title': 'Sample item check RENAME',
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.rename(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(self.user.purpose.first().title, 'Sample item check RENAME')


    def test_update_no_creds(self):
        """Check if unauthorised dude can't update items"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = purpose.update(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_update(self):
        """Check if we can update items"""
        """Check no data"""
        data = json.dumps({})
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.update(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        data = json.dumps({
          'item_id': 11,
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.update(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        data = json.dumps({
          'item_id': 11,
          'title': 'Sample item check UPDATE title',
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.update(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        item1 = Item.objects.create(title='Sample item1', value='Item value 1')
        self.user.purpose.add(item1)
        data = json.dumps({
          'item_id': self.user.purpose.first().id,
          'title': 'Sample item check UPDATE title',
          'value': 'Sample item check UPDATE value',
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.update(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        purpose_item = self.user.purpose.first()
        self.assertEquals(purpose_item.title, 'Sample item check UPDATE title')
        self.assertEquals(purpose_item.value, 'Sample item check UPDATE value')


    def test_destroy_no_creds(self):
        """Check if unauthorised dude can't delete items"""
        request = self.factory.post('/')
        request.user = AnonymousUser()
        request.session = {}
        response = purpose.update(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_destroy(self):
        """Check if we can delete items"""
        """Check no data"""
        data = json.dumps({})
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.destroy(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 400)
        item1 = Item.objects.create(
          title='Sample item to delete',
          value='Item value 1')
        self.user.purpose.add(item1)
        data = json.dumps({
          'item_id': self.user.purpose.first().id,
        })
        request = self.factory.post('/', data, 'application/json')
        request.user = self.user
        response = purpose.destroy(request)
        response_data = json.loads(response.content)
        self.assertEquals(response.status_code, 200)
        purpose_item = self.user.purpose.first()
        self.assertEquals(purpose_item, None)

