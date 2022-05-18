from django.test import TestCase
from hashid_field import Hashid
from accounts.models import User

import logging

class UserModelTest(TestCase):
  """
  Test model fields
  """
  def test_model_str(self):
      user = User.objects.create(
        username='testmodelstring',
        email='testmodelstring@holons.me',
        name='Test model string',
        id=9999,
      )
      self.assertEqual(str(user.id.id), str(9999))

