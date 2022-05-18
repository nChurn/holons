import logging
import copy
from datetime import datetime, timezone, timedelta

from django.core.management.base import BaseCommand

from email_api.helpers.mailbox_helper import random_string_generator
from email_api.models import EmailConversations
from django_mailbox.models import Mailbox as DjangoMailbox
from django_mailbox.models import Message as DjangoMailboxMessage

from django.conf import settings


class Command(BaseCommand):
    help = 'Scan through email database, combine messages into threads'

    FRESH_MESSAGES_TIMESPAN = 10 * 60  # 10 minutes
    # FRESH_MESSAGES_TIMESPAN = 624 * 60 * 60  # 624 hours

    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs
        Get all new MailboxMessage objects not in Conversations
        Loop through each of them
        Guess which message belongs to which Conversation
        Guess if the message starts a new thread/Conversation

        :param args:
        :param options:
        :return:
        """

        logging.info('I am Update Mail Threads command v. 1.0')
        self.make_threads()


    def create_conversation_id(self):
        """
        Used to create cnv_123abc type of id for a conversation
        """

        conv_id_begin = random_string_generator(1,'1234567890')
        conv_id_end = random_string_generator(7, 'abcdefghijklmnopqrstuvxyz')
        return 'cnv_' + conv_id_begin + conv_id_end


    def make_threads(self):
        """
        Collect fresh messages
          √ except message.in_reply_to_id = Null
          √ make a messages_list of each message.id
          √ iterate over messages_list
          √ check if messages in thread have a conversation_id
            √ if not: create a new conversation
            √ else: load existing conversation 
            √ attach messages to the conversation 
        """

        logging.info('Take messages for the given time margin')
        now = datetime.now(timezone.utc)
        diff = now - timedelta(seconds=self.FRESH_MESSAGES_TIMESPAN)

        raw_msgs = DjangoMailboxMessage.objects.filter(processed__gte=diff)\
          .exclude(in_reply_to_id__isnull=True)\
          .order_by('-id')\
          .all()

        logging.info('Raw messages list length: ' + str(len(raw_msgs)))

        messages_threads = []
        for message in raw_msgs:
          messages_threads.append(self.build_thread(message))

        new_conversations_count = 0
        mesages_count = 0
        for single_thread in messages_threads:
          if len(single_thread) > 0: 
            conversation = self.conversation_exists(single_thread)
            if not conversation:
              conversation_id = self.create_conversation_id()
              conversation = EmailConversations.objects.create(
                conversation_id=conversation_id,
                subject=single_thread[len(single_thread) - 1].subject,
                status='unassigned'
              )
              new_conversations_count += 1

            for t_message in single_thread:
              conversation.messages.add(t_message)
              mesages_count += 1

        logging.info('New conversations: ' + str(new_conversations_count)
          + ' messages in threads: ' + str(mesages_count)
        ) 



    def build_thread(self, start_message: DjangoMailboxMessage) -> list:
        """
        Get message, check if it's got in_reply_to_id
        Walk over the in_reply_to_id link, load every message in the thread
        """

        messages_thread = []
        linked_message = self.get_linked_message(start_message.in_reply_to_id)
        if linked_message is not None:
          linked_message = linked_message
          messages_thread.append(linked_message)
          while linked_message is not None:
            linked_message = self.get_linked_message\
              (linked_message.in_reply_to_id)
            if linked_message is not None:
              messages_thread.append(linked_message)
          if linked_message and linked_message.in_reply_to_id is None:
            messages_thread.append(linked_message)
          
        return messages_thread


    def get_linked_message(self, message_id: int) -> DjangoMailboxMessage:
        """
        Load DjangoMailboxMessage by id
        set as a separate method in order to add more logic if needed
        """

        message = DjangoMailboxMessage.objects.filter(pk=message_id).first()
        return message


    def conversation_exists(self, messages_thread: list):
        """
        Check if any of the DjangoMailboxMessage objects in list
        has conversation it's attached to 
        """

        for message in messages_thread:
          if message.conversation.first() is not None:
            return message.conversation.first()


