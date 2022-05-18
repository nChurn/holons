import logging
from model_bakery import baker

from django.test import TestCase
from invitation.models import Token


class TokenModelTest(TestCase):
  """
  Test model fields

  """
  def test_model_unicode_str(self):
      token = baker.make(Token, value='check_token_string', token_type='invitation' )
      self.assertEqual(token.__unicode__(), 'check_token_string : invitation')

