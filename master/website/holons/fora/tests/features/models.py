import logging

from django.test import TestCase
from fora.models import ForaChannel


class UserModelTest(TestCase):
  """
  Test model fields
  """
  def test_fora_channel_model_str(self):
      fora_channel = ForaChannel.objects.create(
        title='Sample title',
      )
      self.assertEqual(str(fora_channel), str('Sample title'))
      self.assertEqual(fora_channel.__unicode__(), str('Sample title'))
