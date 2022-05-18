import datetime
import json
import logging
import os

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import RequestFactory
from django.test import TestCase

import relations.offers as offers
from relations.models import Offer


class OffersTest(TestCase):


    date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
    def setUp(self):
        self.RAY_SOURCES = settings.RAY_SOURCES
        image_path = os.path.join(str(settings.BASE_DIR), "mock/sample_image.jpg")
        userpic = SimpleUploadedFile(name='sample_image.jpg',
          content=open(image_path, 'rb').read(),
          content_type='image/jpeg')
        call_command('loaddata', 'accounts/seed/fixed_users.json', verbosity=0)
        date_stamp = self.date_stamp
        self.password = '12test12'
        self.username = 'test_' + date_stamp

        self.username_second = 'test_wrong' + date_stamp
        self.user_from = get_user_model().objects.create_user(
          username=self.username + '_from',
          password=self.password,
          email=self.username + '_from' + '@holons-test.me',
          phone_number='123'
        )
        self.user_from.userpic = userpic
        self.user_to = get_user_model().objects.create_user(
          username=self.username + '_to',
          password=self.password,
          email=self.username  + '_to' + '@holons-test.me',
          phone_number='222'
        )
        self.user_to.userpic = userpic
        self.user_third = get_user_model().objects.create_user(
          username=self.username + '_third',
          password=self.password,
          email=self.username  + '_third' + '@holons-test.me',
          phone_number='333'
        )
        self.user_third.userpic = userpic
        self.teleport_username = ''
        self.user_from.save()
        self.user_to.save()
        self.user_third.save()
        '''Prepare requests'''
        self.factory = RequestFactory()


    def tearDown(self):
        self.user_from.delete()
        self.user_to.delete()
        self.user_third.delete()


    def test_index_no_creds(self):
        """Test sending a custom message AnonymousUser"""
        url = '/api/relations/offers'
        request = self.factory.get(url)
        request.user = AnonymousUser()
        request.session = {}
        response = offers.index(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_index(self):
        url = '/api/relations/offers'
        """check empty result behavior"""
        request = self.factory.get(url)
        request.user = self.user_from
        response = offers.index(request)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(json.loads(response.content)['data'], [])


    def test_create_no_creds(self):
        """Test sending a custom message AnonymousUser"""
        url = '/api/relations/offers/create'
        request = self.factory.post(url)
        request.user = AnonymousUser()
        request.session = {}
        response = offers.create(request)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, '/auth')


    def test_create(self):
        url = '/api/relations/offers/create'
        """check empty data request"""
        request = self.factory.post(url, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty title')
        """check partial data request"""
        data = {'contractTitle': 'sample title',}
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty from_name')
        """check partial data request"""
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty to_name')
        """check full data request"""
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty terms_from')
        """check partial data request"""
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
          'termsFrom': 'sample terms from',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty terms_to')
        """check partial data request"""
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
          'termsFrom': 'sample terms from',
          'termsTo': 'sample terms to',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty consideration')
        """check partial data request"""
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
          'termsFrom': 'sample terms from',
          'termsTo': 'sample terms to',
          'consideration': 'sample consideration',
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 400)
        self.assertEquals(json.loads(response.content)['message'], 'empty timeframe')
        """check full data request"""
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
          'termsFrom': 'sample terms from',
          'termsTo': 'sample terms to',
          'consideration': 'sample consideration',
          'timeframe': 'sample timeframe',
          'paragraphs': {'part_one': 'first paragraph', 'part_two': 'second paragraph'}
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        self.assertEquals(response.status_code, 200)
        created_offer_id = json.loads(response.content)['data']['id']
        check_offer = self.user_from.offers.filter(pk=created_offer_id).first()
        self.assertEquals(data['contractTitle'], check_offer.title)


    def test_delete(self):
        """Create a valid offer"""
        url = '/api/relations/offers/create'
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
          'termsFrom': 'sample terms from',
          'termsTo': 'sample terms to',
          'consideration': 'sample consideration',
          'timeframe': 'sample timeframe',
          'paragraphs': {'part_one': 'first paragraph', 'part_two': 'second paragraph'}
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        created_offer_id = json.loads(response.content)['data']['id']
      
        """Try to delete (withdraw) the offer"""
        url = '/api/relations/offers/' + str(created_offer_id) + '/delete'
        request = self.factory.delete(url, content_type='application/json')
        request.user = self.user_from
        response = offers.delete(request, created_offer_id)
        withdrawn_offer_status = json.loads(response.content)['data']['status']
        
        self.assertEquals(withdrawn_offer_status, 'withdrawn')


    def test_edit(self):
        """Create a valid offer"""
        url = '/api/relations/offers/create'
        data = {
          'contractTitle': 'sample title',
          'fromName': 'sample from name',
          'toName': 'sample to name',
          'termsFrom': 'sample terms from',
          'termsTo': 'sample terms to',
          'consideration': 'sample consideration',
          'timeframe': 'sample timeframe',
          'paragraphs': {'part_one': 'first paragraph', 'part_two': 'second paragraph'},
        }
        request = self.factory.post(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.create(request)
        created_offer_id = json.loads(response.content)['data']['id']
      
        """Try to delete (withdraw) the offer"""
        url = '/api/relations/offers/' + str(created_offer_id) + '/edit/'
        data = {
          'contractTitle': 'sample title edited',
          'fromName': 'sample from name edited',
          'toName': 'sample to name edited',
          'termsFrom': 'sample terms from edited',
          'termsTo': 'sample terms to edited',
          'consideration': 'sample consideration edited',
          'timeframe': 'sample timeframe',
          'paragraphs': {'part_one': 'first paragraph edited', 'part_two': 'second paragraph edited'},
          'status': 'edited status',
        }
        request = self.factory.patch(url, data, content_type='application/json')
        request.user = self.user_from
        response = offers.edit(request, created_offer_id)
        # edited_offer = json.loads(response.content)['data']
        # 
        # self.assertEquals(edited_offer.contractTitle, 'sample title edited')
        # self.assertEquals(edited_offer.termsFrom, 'sample terms from edited')
        # self.assertEquals(edited_offer.termsTo, 'sample terms to edited')
        # self.assertEquals(edited_offer.consideration, 'sample consideration edited')
        # self.assertEquals(edited_offer.timeframe, 'sample timeframe')
