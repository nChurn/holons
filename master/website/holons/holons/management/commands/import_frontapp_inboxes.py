from django.core.management.base import BaseCommand
import logging
import datetime
import json
import requests
import base64
import sys
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

from django.utils import timezone
from django_mailbox.models import Message as DjangoMailboxMessage
from django_mailbox.models import Mailbox as DjangoMailbox
from email_api.models import Mailbox
from email_api.models import EmailSettings
from email_api.models import EmailImportStatus
from email_api.models import EmailConversations
from email_api.models import MailMessageStatus


def fetch_inboxes_list(token: str) -> list:
    """
    Take token, send API request, return a {name, id} list of inboxes

    :param token:
    :return:
    """

    logging.info('Get inboxes')
    auth_header = 'Bearer ' + token
    headers = {"content-type": "application/json", 'Authorization': auth_header}
    inbox_api_url = 'https://api2.frontapp.com/inboxes'
    response = json.loads(requests.request("GET", inbox_api_url, headers=headers).text)
    inboxes = []
    for element in response.get('_results', None):
        inboxes.extend([{'name': element.get('send_as', None), 'id': element.get('id', None)}])

    return inboxes


def get_mailbox_by_name(mailbox_name):
    mailbox = Mailbox.objects.filter(incoming_email=mailbox_name).first()
    return mailbox


def update_import_status(
        mailbox_name: str = '',
        status: str = '',
        conversation_count: int = 0,
        message_count: int = 0,
        started_at: datetime.datetime = None,
        completed_at: datetime.datetime = None,
):
    if mailbox_name != '':
        mailbox = get_mailbox_by_name(mailbox_name)
        import_status = EmailImportStatus.objects.filter(mailbox_id=mailbox.id).first()
        if conversation_count != 0:
            import_status.conversation_count += conversation_count
        if message_count != 0:
            import_status.message_count += message_count
        if status != '':
            import_status.status = status
        if started_at is not None:
            import_status.started_at = started_at
        if completed_at is not None:
            import_status.completed_at = completed_at

        import_status.save()

    pass


def store_conversation(conversation, mailbox_name: str = ''):
    conversation_record, created = EmailConversations.objects.get_or_create(
        conversation_id=conversation.get('id'),
        subject=conversation.get('subject'),
        status=conversation.get('status'),
    )
    if created is True:
        logging.info('conversation saved')
        update_import_status(mailbox_name=mailbox_name, status='', conversation_count=1)
    pass


def fetch_conversations(mailbox: dict, token: str, pagination_link: str = '', conversations: list = []) -> list:
    """
    Get a mailbox and a token
    Call API get a list of conversations
    Form a {id, subject, inbound} list of conversations
    Check if the conversations are paginated
        — if paginated, remember processed work
        — call the same function recursively
        — pass the next page link

    :param mailbox:
    :param token:
    :param pagination_link:
    :param conversations:
    :return:
    """

    auth_header = 'Bearer ' + token
    headers = {"content-type": "application/json", 'Authorization': auth_header}
    if pagination_link == '':
        inbox_api_url = 'https://api2.frontapp.com/inboxes/' + mailbox['id'] + '/conversations'
    else:
        inbox_api_url = pagination_link
    response = json.loads(requests.request("GET", inbox_api_url, headers=headers).text)
    count_conversations = len(conversations)
    for conversation in response.get('_results'):
        conversations.extend([{
            'id': conversation.get('id'),
            'subject': conversation.get('subject'),
            'status': conversation.get('status')
        }])
        count_conversations += 1
        store_conversation(conversation, mailbox['name'])

    ''' Check if we have more pages '''
    if response.get('_pagination') is not None:
        pagination = response.get('_pagination')
        if pagination.get('next', None) is not None:
            fetch_conversations(mailbox, token, pagination.get('next', None), conversations)

    logging.info('Fetch conversations for the inbox ' + mailbox['id'] + ' (' + mailbox['name'] + ')')
    logging.info('count conversations: ' + str(count_conversations))
    return conversations


def fetch_messages(conversation: dict, token: str, pagination_link: str = '', messages: list = []) -> list:
    """
    Get a conversation and a token
    Call API get a list of messages in the conversation
    Form a {id, subject, inbound} list of conversations
    {id, subject, author, recipients, author_email, body, inbound}
    Check if the conversations are paginated
        — if paginated, remember processed work
        — call the same function recursively
        — pass the next page link


    :param conversation:
    :param token:
    :param pagination_link:
    :param messages:
    :return:
    """
    auth_header = 'Bearer ' + token
    headers = {"content-type": "application/json", 'Authorization': auth_header}
    if pagination_link == '':
        conversation_api_url = 'https://api2.frontapp.com/conversations/' + conversation['id'] + '/messages'
    else:
        conversation_api_url = pagination_link
    response = json.loads(requests.request("GET", conversation_api_url, headers=headers).text)
    count_messages = len(messages)
    for message in response.get('_results'):
        author = ''
        if message.get('author') is not None:
            author_object = message.get('author')
            author += '' + author_object.get('first_name') + ' ' + author_object.get('first_name')
            author += ' <' + author_object.get('email') + '>'
        mail_to = ''
        mail_from = ''
        if message.get('recipients') is not None:
            for recipient in message.get('recipients'):
                if recipient.get('role') == 'to':
                    mail_to += recipient.get('handle') + ' '
                if recipient.get('role') == 'from':
                    mail_from += recipient.get('handle') + ' '
                logging.info(str(recipient.get('role')) + ': ' + recipient.get('handle'))
        messages.extend([{
            'id': message.get('id'),
            'subject': message.get('subject'),
            'author': author,
            'created_at': message.get('created_at'),
            'mail_to': mail_to,
            'mail_from': mail_from,
            'author_email': message.get('author.email'),
            'body': message.get('body'),
            'inbound': message.get('is_inbound'),
            'related': message.get('related')
        }])
        count_messages += 1

    ''' Check if we have more pages '''
    if response.get('_pagination') is not None:
        pagination = response.get('_pagination')
        if pagination.get('next', None) is not None:
            logging.info('Going deeper. Messages count:' + str(count_messages))
            messages = []
            fetch_messages(conversation, token, pagination.get('next', None), messages)

    logging.info('Fetch messages for the conversation ' + conversation['id'] + ' (' + conversation['subject'] + ')')
    # logging.info('messages count: ' + str(count_messages))
    #     time.sleep(1)
    return messages


def store_messages(mailbox_id, messages, mailbox_name: str = '', conversation=None):
    conversation_object = None
    if conversation is not None:
        conversation_object = EmailConversations.objects.filter(conversation_id=conversation.get('id')).first()

    for message in messages:
        outgoing = True
        if message['inbound'] == 'true':
            outgoing = False

        tz = datetime.datetime.now(datetime.timezone(datetime.timedelta(0))).astimezone().tzinfo
        created_at_date = datetime.datetime.fromtimestamp(message['created_at'], tz=tz)\
            .strftime('%Y-%m-%d %H:%M:%S.%f%z')

        message_exists = DjangoMailboxMessage.objects.filter(message_id=message['id'])
        if len(message_exists) == 0:  # create_or_update was causing error
            mail_message = DjangoMailboxMessage.objects.create(
                subject=message['subject'],
                message_id=message['id'],
                from_header=message['mail_from'],
                to_header=message['mail_to'],
                outgoing=outgoing,
                body=base64.b64encode(message['body'].encode('utf-8')).decode('ascii'),
                processed=str(created_at_date),
                read=str(created_at_date),
                encoded=True,
                mailbox_id=mailbox_id,
                in_reply_to_id=None,
            )
            mail_message.save()
            if conversation_object is not None:
                conversation_object.messages.add(mail_message)
            update_import_status(mailbox_name=mailbox_name, status='', conversation_count=0, message_count=1)
        else:  # update message status
            stored_message = DjangoMailboxMessage.objects.filter(message_id=message['id']).first()
            logging.info('Import message')
            logging.info(conversation['status'])
            message_status, created = MailMessageStatus.objects.get_or_create(
                message_id=stored_message.id,
            )
            if conversation['status'] == 'archived':
                message_status.is_archived = True
            if conversation['status'] == 'deleted':
                message_status.is_deleted = True
            message_status.save()

    pass


def get_mailboxes_from_queue() -> list:
    """
    √ Loop through EmailImportStatus, take first records with unique frontapp_token && status != complete
    :return:
    """

    mailboxes = EmailImportStatus.objects.exclude(status='complete').order_by('-created_at')
    logging.info('Total number of mailboxes in the import queue: ' + str(len(mailboxes)))
    sorted_mailboxes = {}
    mailboxes_dict = []
    for mailbox in mailboxes:
        sorted_mailboxes[mailbox.mailbox.frontapp_token] = mailbox.mailbox.incoming_email
    for mailbox in sorted_mailboxes:
        mailboxes_dict.extend([{'token': mailbox, 'inbox_name': sorted_mailboxes[mailbox]}])

    return mailboxes_dict


def refresh_import_queue():
    """
    √ Get all Mailboxes with import_frontapp_inboxes == True && import_frontapp_inboxes != ''
    √ Loop through the mailboxes add to the EmailImportStatus those, having at least 1 Message e.g. Active
    :return:
    """

    logging.info('Refresh import queue')
    mailboxes_to_import = Mailbox.objects.filter(is_frontapp_import=True).filter(frontapp_token__isnull=False)
    count_new = 0
    for mailbox in mailboxes_to_import:
        messages = DjangoMailbox.objects.filter(name=mailbox.name.split('@')[0]).first().messages.all()
        if len(messages) > 0:
            status, created = EmailImportStatus.objects.get_or_create(
                    mailbox_id=mailbox.id,
            )
            if created:
                count_new += 1
    logging.info('New mailboxes added to import queue: ' + str(count_new))
    pass


def import_mailbox(mailbox):
    logging.info('Start import MAILBOX')
    mailbox_list = fetch_inboxes_list(mailbox['token'])

    inbox_to_import = next((item for item in mailbox_list if item['name'] == mailbox['inbox_name']), None)
    if inbox_to_import is not None:
        logging.info('import inbox ' + inbox_to_import['name'])
        started_at = timezone.now()

        update_import_status(
            mailbox_name=mailbox['inbox_name'],
            status='started',
            started_at=started_at,
        )
        conversations_list = fetch_conversations(inbox_to_import, mailbox['token'])
        for conversation in conversations_list:
            messages = fetch_messages(conversation, mailbox['token'])
            mailbox_object = get_mailbox_by_name(inbox_to_import['name'])
            mailbox_id = DjangoMailbox.objects.filter(from_email=mailbox_object.name).first()
            store_messages(str(mailbox_id.id), messages, inbox_to_import['name'], conversation)

        completed_at = timezone.now()

        update_import_status(
            mailbox_name=mailbox['inbox_name'],
            status='complete',
            completed_at=completed_at
        )


class Command(BaseCommand):
    help = 'Get EmailSettings from the database, query Frontapp API, save contents to the database'

    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs

        v. 2.0

            √ 1. Get all Mailboxes with import_frontapp_inboxes == True && import_frontapp_inboxes != ''
            √ 2. Loop through the mailboxes add to the EmailImportStatus those, having at least 1 Message e.g. Active
            √ 3. Loop through EmailImportStatus, take first records with unique frontapp_token && status != complete
            √ 4. Start import for each of selected Mailboxes in parallel, use map(fetch_mailbox, mailbox_list), maybe?
            √ 5. On every import update EmailConversations for given Mailbox and EmailImportStatus.conversation_count
            √ 6. On every Message import update EmailImportStatus.message_count
            √ 7. Do not import Messages twice (message_id=unique)
            √ 8. On import of the last Message, set EmailImportStatus.status = complete

        :param args:
        :param options:
        :return:
        """

        logging.info('I am import_frontapp_inboxes command')
        logging.info('I write results to: mail messages database')
        logging.info('Getting mailboxes to import')
        refresh_import_queue()
        mailboxes = get_mailboxes_from_queue()

        pool = ThreadPool(4)
        results = pool.map(import_mailbox, mailboxes)
        # import_mailbox(mailboxes)

        '''
        v. 1.0 
            Get all user EmailSettings
            √ Loop through EmailSettings, query API for all inboxes for each of the Frontapp Token
            √ Get all Mailbox objects having is_frontapp_import = True
            √ Loop through each of them, match local inbox name with Frontapp id
            √ Call fetch method for each mailbox id
            √ Store messages for each inbox
        
        mailboxes_to_import = Mailbox.objects.filter(is_frontapp_import=True)
        logging.info('Number of inboxes to process): ' + str(len(mailboxes_to_import)))
        email_settings = EmailSettings.objects.all()
        logging.info('Number of Frontapp Tokens to process): ' + str(len(email_settings)))
        for setting in email_settings:
            user_mailboxes = setting.users.first().mailboxes.filter(is_frontapp_import=True)
            mailbox_list = fetch_inboxes_list(setting.frontapp_token)
            for mailbox in user_mailboxes:
                inbox_to_import = next((item for item in mailbox_list if item['name'] == mailbox.incoming_email), None)
                if inbox_to_import is not None:
                    conversations_list = fetch_conversations(inbox_to_import, setting.frontapp_token)
                    for conversation in conversations_list:
                        messages = fetch_messages(conversation, setting.frontapp_token)
                        mailbox_id = DjangoMailbox.objects.filter(from_email=mailbox.name).first()
                        store_messages(str(mailbox_id.id), messages)
        '''

