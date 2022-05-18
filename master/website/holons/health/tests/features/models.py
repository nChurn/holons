import datetime

from django.test import TestCase
from django.utils import timezone
from health.models import *

import logging

class HealthModelsTest(TestCase):
  """
  Test model fields
  """
  now = timezone.now()


  def SetUp(self):
      pass


  def test_log_model_str(self):
      log = Log.objects.create(
        event_type='sample event type',
        check_date=self.now
      )
      self.assertEqual(str(log), 'sample event type ' + str(log.check_date))
      self.assertEqual(log.__unicode__(), 'sample event type ' + str(log.check_date))


  def test_talent_stat_model_str(self):
      talent_stat = TalentStat.objects.create(
        messages_master=100500,
        messages_rays=100,
        check_date=self.now
      )
      self.assertEqual(str(talent_stat), '100500 : 100 ' + str(talent_stat.check_date))
      self.assertEqual(talent_stat.__unicode__(), '100500 : 100 ' + str(talent_stat.check_date))

