import logging
import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

from email_api.models import *

class EmailModelsTest(TestCase):
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
  def test_mailbox_model_str(self):
      mailbox = Mailbox.objects.create(
        name='Sample name',
      )
      self.assertEqual(str(mailbox), 'Sample name')
      self.assertEqual(mailbox.__unicode__(), 'Sample name')


  def test_shared_mail_message_model_str(self):
      shared_mail_message = SharedMailMessage.objects.create(
        assigned_to_id = self.user_from.id,
        assigned_by_id = self.user_to.id,
        mailbox_from_id=1,
        mailbox_to_id=2,
      )
      self.assertEqual(str(shared_mail_message), 'from: 1 to: 2')
      self.assertEqual(shared_mail_message.__unicode__(), 'from: 1 to: 2')


  def test_email_conversations_model_str(self):
      email_conversation = EmailConversations.objects.create(
        conversation_id='conversation_id',
      )
      self.assertEqual(str(email_conversation), 'conversation_id')
      self.assertEqual(email_conversation.__unicode__(), 'conversation_id')


  def test_mail_message_status_model_str(self):
      mail_message_status = MailMessageStatus.objects.create(
        pk=999,
      )
      self.assertEqual(str(mail_message_status), '999')
      self.assertEqual(mail_message_status.__unicode__(), '999')


  def test_email_import_status_model_str(self):
      mailbox = Mailbox.objects.create(
        name='Sample name',
      )
      email_import_status = EmailImportStatus.objects.create(
        mailbox=mailbox
      )
      self.assertEqual(str(email_import_status), mailbox.name)
      self.assertEqual(email_import_status.__unicode__(), mailbox.name)


