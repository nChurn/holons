import logging
import base64

from typing import Union, Set, Optional
from django.db.models.query import QuerySet
from django.db.models import Subquery
from django_mailbox.models import Message as DjangoMailboxMessage
from email_api.models import Mailbox
from email_api.models import EmailConversations
from email_api.models import MailMessageStatus
from email_api.models import SharedMailMessage


def get_new_messages_count(mailbox_id: int) -> int:
    count = 0
    all_messages = DjangoMailboxMessage.objects.filter(mailbox_id=mailbox_id)
    all_conversations = EmailConversations.objects\
        .filter(messages__in=Subquery(all_messages.values('id')))

    # logging.info('============')
    # logging.info('Mailbox: ' + str(len(all_messages)))
    # logging.info('Messages: ' + str(len(all_messages)))
    # logging.info('Conversations: ' + str(len(all_conversations)))
    # for conversation in all_conversations:
    #   conversation_checked = False
    #   for message in all_messages:
    #     message_status = get_message_status(message.id)
    #     if message_status is None and message in conversation.messages.all():
    #     # if message in conversation.messages.all() and message_status != conversation.status: #  or message not in conversation.messages:
    #       count += 1


    return count


def decode_message(message: QuerySet, conversation_id: Union[bool, str], message_status: str) -> list:
    message_body = message.text
    if message.html != '':
        message_body = message.html
    decoded_message = [{
        'conversation': conversation_id,
        'html': message_body.replace("\\ufffd",''),
        'from_address': message.from_address,
        'to_address': message.to_addresses,
        'subject': message.subject.replace("\\ufffd",''),
        'message_id': message.message_id,
        'read': message.read,
        'id': message.id,
        'processed': message.processed,
        'status': message_status,
        'outgoing': message.outgoing,
    }]
    return decoded_message


def get_message_status(message_id: int):
    """
    Wrapper to check for a message status

    :param message_id:
    :return:
    """
    message_status = MailMessageStatus.objects.filter(message_id=message_id).first()
    
    if message_status is not None:
        if message_status.is_deleted:
            return 'deleted'
        if message_status.is_archived:
            return 'archived'
        if message_status.is_snoozed:
            return 'snoozed'
    return None


def save_message(mailbox_id, subject, message_id, in_reply_to_id, from_header, to_header, body):
    DjangoMailboxMessage.objects.create(
        mailbox_id=mailbox_id,
        subject=subject,
        message_id=message_id,
        in_reply_to_id=in_reply_to_id,
        from_header=from_header,
        to_header=to_header,
        outgoing=True,
        body=base64.b64encode(body.encode('utf-8')).decode('ascii'),
        encoded=True,
        eml=None
    )

def get_shared_threads(mailbox: Mailbox) -> dict:
    """
    This takes mailbox and looks for the messages/threads
    shared with the mailbox id
    returns dict of threads/messages lists
    """

    threads = SharedMailMessage.objects.filter(mailbox_to_id=mailbox.id)
    formatted_threads = {}
    formatted_messages = []
    """ Get shared threads for mailbox """
    for thread in threads:
      if thread.messages.all():
        '''
          we use ManyToMany as a ForeignKey, it's an overkill now, 
          but we shall need it in case we have to share individual messages
        '''
        mailbox_from = Mailbox.objects.filter(pk=thread.mailbox_from_id).first()
        messages = thread.messages
        conversations = EmailConversations.objects\
            .filter(messages__in=Subquery(messages.values('id')))
        if conversations:
          for conversation in conversations:
            conversation_id = conversation.conversation_id
            message_status = conversation.status
            formatted_threads[conversation_id] = []
            for message in conversation.messages.all():
              decoded_message = decode_message(message, conversation_id, message_status)
              formatted_threads[conversation_id].extend(decoded_message)
        else:
          message = messages.first()
          decoded_message = decode_message(message, False, get_message_status(message.id))
          decoded_message[0]['subject'] = '[' + mailbox_from.incoming_email + ' >> ' + mailbox.incoming_email +  '] ' + decoded_message[0]['subject']
          formatted_messages.extend(decoded_message)
    return { 'shared_threads': formatted_threads, 'shared_messages': formatted_messages }

