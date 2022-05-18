import logging
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from moneta.models import *

class MonetaModelsTest(TestCase):
  date_stamp = str(datetime.datetime.now().timestamp()).split('.')[0][0:8]
  def setUp(self):
      date_stamp = self.date_stamp
      self.password = '12test12'
      self.username = 'test_' + date_stamp

      self.user_from = get_user_model().objects.create_user(
        username=self.username,
        password=self.password,
        email=self.username + '@holons-test.me',
        phone_number='123'
      )
      self.user_from.save()

      self.user_to = get_user_model().objects.create_user(
        username=self.username + '_to',
        password=self.password,
        email=self.username + '_to@holons-test.me',
        phone_number='222'
      )
      self.user_to.save()
      '''Prepare requests'''


  def tearDown(self):
      self.user_from.delete()
      self.user_to.delete()


  """
  Test model fields
  """
  def test_business_entity_model_str(self):
      business_entity = BusinessEntity.objects.create(
        name='Sample name',
      )

      self.user_from.entities.add(business_entity)
      self.assertEqual(str(business_entity), 'Sample name')
      self.assertEqual(business_entity.__unicode__(), 'Sample name')


