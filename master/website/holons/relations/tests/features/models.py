import logging

from django.test import TestCase
from relations.models import *


class RelationsModelsTest(TestCase):
  """
  Test model fields
  """
  def test_offer_model_str(self):
      offer = Offer.objects.create(
        title='Sample offer',
        from_name='Sample from name',
        to_name='Sample to name',
      )
      self.assertEqual(str(offer), str('Sample from name -> Sample to name'))
      self.assertEqual(offer.__unicode__(), str('Sample from name -> Sample to name'))

