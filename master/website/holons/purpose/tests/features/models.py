import logging

from django.test import TestCase
from purpose.models import Item


class ItemModelTest(TestCase):
  """
  Test model fields
  """
  def test_item_model_str(self):
      item = Item.objects.create(
        title='test title',
        value='test value',
      )
      self.assertEqual(str(item), 'test title : test value')
      self.assertEqual(item.__unicode__(), 'test title : test value')


