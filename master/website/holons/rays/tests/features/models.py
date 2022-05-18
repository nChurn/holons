import logging
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from rays.models import *

class RaysModelsTest(TestCase):
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
  def test_talent_model_str(self):
      talent = Talent.objects.create(
        name='Sample name',
      )
      self.assertEqual(str(talent), 'Sample name')
      self.assertEqual(talent.__unicode__(), 'Sample name')


  def test_upwork_talent_model_str(self):
      source = RaySource.objects.create(
        pk=0,
        title='empty source'
      )
      talent = UpworkTalent.objects.create(
        title='Sample title',
      )
      self.assertEqual(str(talent), 'Sample title')
      self.assertEqual(talent.__unicode__(), 'Sample title')


  def test_ray_template_model_str(self):
      ray_template = RayTemplate.objects.create(
        title='Sample title',
      )
      self.assertEqual(str(ray_template), 'Sample title')
      self.assertEqual(ray_template.__unicode__(), 'Sample title')
      

  def test_ray_source_model_str(self):
      ray_source = RaySource.objects.create(
        title='Sample title',
      )
      self.assertEqual(str(ray_source), 'Sample title')
      self.assertEqual(ray_source.__unicode__(), 'Sample title')

      
  def test_direct_message_model_str(self):
      direct_message = DirectMessage.objects.create(
        subject='Sample subject',
      )
      self.assertEqual(str(direct_message), 'Sample subject')
      self.assertEqual(direct_message.__unicode__(), 'Sample subject')

      
  def test_client_stats_model_str(self):
      client_stats = ClientStats.objects.create(
        guid='Sample guid',
      )
      self.assertEqual(str(client_stats), 'Sample guid')
      self.assertEqual(client_stats.__unicode__(), 'Sample guid')

      
  def test_custom_talent_model_str(self):
      custom_talent = CustomTalent.objects.create(
        title='Sample title',
      )
      self.assertEqual(str(custom_talent), 'Sample title')
      self.assertEqual(custom_talent.__unicode__(), 'Sample title')


  def test_ray_model_str(self):
      ray = Ray.objects.create(
        pk=9999,
      )
      self.assertEqual(str(ray), '9999')
      self.assertEqual(ray.__unicode__(), '9999')


  def test_message_assigned_model_str(self):
      ray_source = RaySource.objects.create(
        pk=0,
        title='Sample title',
      )
      message = UpworkTalent.objects.create(
        title='test subject'
      )
      message_assigned = MessageAssigned.objects.create(
        message=message,
        owner=self.user_from.id,
        assignee=self.user_to.id
      )
      self.assertEqual(str(message_assigned), 'test subject')
      self.assertEqual(message_assigned.__unicode__(), 'test subject')


  def test_message_thread_model_str(self):
      thread = MessageThread.objects.create(pk=999)
      self.assertEqual(str(thread), '999')
      self.assertEqual(thread.__unicode__(), '999')


  def test_ray_canned_model_str(self):
      ray_canned = RayCanned.objects.create(title='sample title')
      self.assertEqual(str(ray_canned), 'sample title')
      self.assertEqual(ray_canned.__unicode__(), 'sample title')

