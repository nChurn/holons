import logging
import json
import time
import sys

from typing import Union, Set, Optional
from django.http import HttpRequest, JsonResponse
from django.conf import settings
from django.core.mail import message as emailMessage
from django.core.management import call_command
from django.db.models import Subquery

from .helpers import request_helper
from .helpers import auth_helper
from .helpers import mailbox_helper
from .helpers import message_helper
from .helpers import sendgrid_helper
from .helpers import email_helper

from .models import Mailbox
from .models import MailMessageStatus
from .models import EmailConversations
from .models import SharedMailMessage
from accounts.models import User
from django_mailbox.models import Mailbox as DjangoMailbox
from django_mailbox.models import Message as DjangoMailboxMessage

"""
    Mailbox-related API requests
"""


def user_send_email(request: HttpRequest) -> JsonResponse:
    """
    Send email using SendGrid
    :param mailbox_name:
    :return:
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    if str(user) == 'AnonymousUser':
        return JsonResponse({'error': 'Not authorized'}, status=403)
    if method == 'post':
        ''' get email fields '''
        data = json.loads(request.body)
        email_helper.send_email(
            data['from'],
            data['to'],
            data['subject'],
            data['message']
        )

        mailbox = DjangoMailbox.objects.filter(from_email=data['mailboxAlias']).first()

        domain_name = mailbox_helper.account_create_incoming_domain(data['from'])
        message_id = emailMessage.make_msgid(domain=domain_name)
        message_helper.save_message(
          mailbox.id,
          data['subject'],
          message_id,
          data.get('inReplyToId', None),
          data['from'],
          data['to'],
          data['message']
        )
        if data.get('conversationId', False):
            conversation_object = EmailConversations.objects\
                .filter(conversation_id=data.get('conversationId', None)).first()
            conversation_object.messages.add(message)

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'data': data,
    })


def user_get_all_unread_messages(request: HttpRequest) -> JsonResponse:
    """
    Return all unread messages for the logged in user
    """

    user = auth_helper.get_user(request)
    if not request.user.is_authenticated:
      return JsonResponse({
          'result': 'OK',
          'messages': [],
          'messages_count': 0,
          'shared' : {
            'shared_threads': [],
            'shared_messages': []
          }
      })

    mailboxes = user.mailboxes.all()
    mailboxes_ids = []
    messages = []
    # @todo: this is extensive
    # move data logic to the models
    for mailbox in mailboxes:
        django_mailbox = DjangoMailbox.objects.filter(name=mailbox.name.split('@')[0]).first()
        mailboxes_ids.append(django_mailbox.id)

    messages = DjangoMailboxMessage.objects\
      .filter(mailbox_id__in=mailboxes_ids)\
      .filter(read__isnull=True)\
      .order_by('-id')

    # that's a hack to make local development faster, limit 20mb JSONs to 100 items 
    hostname = request.get_host()[:9]
    if 'localhost' == hostname:
        messages = messages[0:100]

    decoded_messages = []
    for message in messages:
        conversation_id = False
        conversation = EmailConversations.objects.filter(messages__id__exact=message.id).first()
        if conversation:
            conversation_id = conversation.conversation_id
            message_status = conversation.status
        else:
            message_status = message_helper.get_message_status(message.id)
        if not message_status:
          decoded_message = message_helper.decode_message(message, conversation_id, message_status)
          decoded_message[0]['mailbox_alias'] = message.mailbox.from_email
          decoded_messages.extend(decoded_message)

    messages_length = len(decoded_messages)

    return JsonResponse({
        'result': 'OK',
        'messages': decoded_messages[0:500],
        'messages_count': messages_length,
        'shared' : {
          'shared_threads': [],
          'shared_messages': []
        }
    })


def user_mailboxes_list(request: HttpRequest) -> JsonResponse:
    """
    Return only mailboxes and their status, no messages
    - In case we have search_string parameter, return only mailboxes having:
     1) message-threads with domain matching search_string
     2) message-threads with body text having search_string
     3) ... (additional search behaviours to be added here)

     @todo: this is a candidate for refactoring, rewrite to use user_get_mailbox_messages 

    :param request:
    :return:
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    mailboxes = {'active': [], 'pending': []}

    if not request.user.is_authenticated:
      return JsonResponse({
          'result': 'OK',
          'method': method,
          'mailboxes': mailboxes,
      })

    search_string = request.GET.get('search_string', '')
    if search_string != '':
        logging.info('Search string: ' + search_string)

    for mailbox in user.mailboxes.all().filter(is_active=True).order_by('incoming_email'):
        django_mailbox = DjangoMailbox.objects.filter(name=mailbox.name.split('@')[0]).first()
        messages = None
        if django_mailbox:
            if search_string == '':
                messages = DjangoMailboxMessage.objects.filter(mailbox_id=django_mailbox.id).order_by('-id')
            else:
                messages = DjangoMailboxMessage.objects\
                    .filter(mailbox_id=django_mailbox.id)\
                    .filter(to_header__icontains=search_string).order_by('-id')
                if len(messages) == 0:
                    messages = DjangoMailboxMessage.objects \
                        .filter(mailbox_id=django_mailbox.id).order_by('-id')

                    if len(messages) > 0:
                        ''' Search inside encoded email bodies '''
                        filtered_messages = DjangoMailboxMessage.objects.none()
                        for message in messages:
                            if search_string in message.text:
                                filtered_messages |= DjangoMailboxMessage.objects.filter(pk=message.id)
                        messages = filtered_messages

            messages_count = message_helper.get_new_messages_count(django_mailbox.id)



        if messages:
            mailboxes['active'].extend([{
                'id': mailbox.id,
                'name': mailbox.name,
                'domain': mailbox.domain,
                'alias': mailbox.incoming_email.split('@')[0],
                'incoming_email': mailbox.incoming_email,
                'messages': [],
                'messages_count': messages_count,
                'status': mailbox.is_active,
                'is_verified': mailbox.is_verified,
                'is_paused': mailbox.is_paused,
                'dns': {
                    'dkim1': mailbox.dns_dkim1,
                    'dkim1_data': mailbox.dns_dkim1_data,
                    'dkim2': mailbox.dns_dkim2,
                    'dkim2_data': mailbox.dns_dkim2_data,
                    'mail_cname': mailbox.dns_mail_cname,
                    'mail_cname_data': mailbox.dns_mail_cname_data,
                    'is_verified': mailbox.is_verified
                },
            }])
        else:
            mailboxes['pending'].extend([{
                'id': mailbox.id,
                'name': mailbox.name,
                'domain': mailbox.domain,
                'alias': mailbox.incoming_email.split('@')[0],
                'incoming_email': mailbox.incoming_email,
                'dkim1': mailbox.dns_dkim1,
                'dkim1_data': mailbox.dns_dkim1_data,
                'dkim2': mailbox.dns_dkim2,
                'dkim2_data': mailbox.dns_dkim2_data,
                'mail_cname': mailbox.dns_mail_cname,
                'mail_cname_data': mailbox.dns_mail_cname_data,
                'status': mailbox.is_active,
                'is_verified': mailbox.is_verified,
                'is_paused': mailbox.is_paused,
            }])
    return JsonResponse({
        'result': 'OK',
        'method': method,
        'mailboxes': mailboxes,
    })


def user_get_mailbox_messages(request: HttpRequest) -> JsonResponse:
    """
    Retrieve and format messages for a single mailbox

    :param request:
    :return:
    """

    search_string = request.GET.get('search_string', '')
    if search_string != '':
        logging.info('Search string: ' + search_string)

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    mailbox_name = data.get('mailbox_name', None)
    mailbox_list = []

    mailbox = Mailbox.objects.filter(name=mailbox_name).first()
    django_mailbox = DjangoMailbox.objects.filter(name=mailbox_name.split('@')[0]).first()
    messages = None
    conversations_messages = {}

    if django_mailbox:
        if search_string == '':
            messages = DjangoMailboxMessage.objects.filter(mailbox_id=django_mailbox.id).order_by('-id')
        else:
            messages = DjangoMailboxMessage.objects \
                .filter(mailbox_id=django_mailbox.id) \
                .filter(to_header__icontains=search_string).order_by('-id')
        if len(messages) == 0:
            messages = DjangoMailboxMessage.objects \
                .filter(mailbox_id=django_mailbox.id).order_by('-id')

            if len(messages) > 0:
                filtered_messages = DjangoMailboxMessage.objects.none()
                for message in messages:
                    if search_string in message.text:
                        filtered_messages |= DjangoMailboxMessage.objects.filter(pk=message.id)
                messages = filtered_messages

        conversations = EmailConversations.objects.filter(messages__in=Subquery(messages.values('id')))
        for conversation in conversations:
            conversations_messages[conversation.conversation_id] = []

    if messages:
        decoded_messages = []
        messages_count = 0
        for message in messages:
            # @todo: fix this, remove obsolete checks
            conversation_id = False
            conversation = EmailConversations.objects.filter(messages__id__exact=message.id).first()
            if conversation:
                conversation_id = conversation.conversation_id
                message_status = conversation.status
            else:
                message_status = message_helper.get_message_status(message.id)

            if message_status is None:
                messages_count += 1

            decoded_message = message_helper.decode_message(message, conversation_id, message_status)
            if conversation:
                conversation_id = conversation.conversation_id
                conversations_messages[conversation_id].extend(decoded_message)
            else:
                decoded_messages.extend(decoded_message)


        ''' look for shared threads/messages '''
        logging.info('look for shared threads/messages')
        shared = message_helper.get_shared_threads(mailbox)

        mailbox_list.extend([{
            'id': mailbox.id,
            'name': mailbox.name,
            'domain': mailbox.domain,
            'alias': mailbox.incoming_email.split('@')[0],
            'incoming_email': mailbox.incoming_email,
            'messages': list(decoded_messages),
            'conversations': conversations_messages,
            'shared': shared,
            'messages_count': messages_count,
            'status': mailbox.is_active,
            'is_paused': mailbox.is_paused,
            'dns': {
                'dkim1': mailbox.dns_dkim1,
                'dkim1_data': mailbox.dns_dkim1_data,
                'dkim2': mailbox.dns_dkim2,
                'dkim2_data': mailbox.dns_dkim2_data,
                'mail_cname': mailbox.dns_mail_cname,
                'mail_cname_data': mailbox.dns_mail_cname_data,
                'is_verified': mailbox.is_verified
            },
        }])


    return JsonResponse({
        'result': 'OK',
        'method': method,
        'mailbox': mailbox_list,
    })


def create_mailbox_item(request: HttpRequest, user) -> JsonResponse:
    """

    :param user:
    :param request:
    :return:
    """

    ''' get mailbox name '''
    data = json.loads(request.body)
    mailbox_name = data.get('mailbox', None)
    if mailbox_name is None or mailbox_name == '':
        mailbox_name = mailbox_helper.random_string_generator(20) + '@holons.me'
    is_frontapp_import = data.get('frontapp_import', False)
    frontapp_token = data.get('frontapp_token', None)
    incoming_mailbox_name = data['incoming_email']  # @todo: add some validation to make sure we have real email
    ''' create inbox record if it not exists '''
    mailbox, created = Mailbox.objects.get_or_create(
        name=mailbox_name,
        domain=mailbox_helper.account_create_incoming_domain(incoming_mailbox_name)
    )
    mailbox_message = mailbox_name + ' created'
    ''' attach django user to the mailbox '''
    user_object = User.objects.filter(pk=user.id).first()
    ''' create modoboa mailbox for the user '''
    user_object.mailboxes.add(mailbox.id)
    ''' check if email account for a given mailbox exists '''
    if not mailbox_helper.account_exists(mailbox_name):
        ''' — create new email account via API '''
        mailbox_helper.account_create(mailbox_name)

    ''' check if django_mailbox mailbox account for this user/mailbox '''
    if not DjangoMailbox.objects.filter(name=mailbox_name.split('@')[0]):
        ''' — create django_mailbox mailbox account for this user/mailbox '''
        mailbox_helper.user_create_django_mailbox(mailbox_name)

    ''' fill up and save user_mailbox with data from SendGrid API (necessary to keep track of dns-records) '''
    if mailbox.sendgrid_subuser == '':
        mailbox.incoming_email = incoming_mailbox_name.replace(' ', '')
        mailbox.name = mailbox_name
        domain_meta = mailbox_helper.user_mailbox_confirm_use(mailbox.domain, mailbox_name)
        logging.info(domain_meta)
        mailbox.dns_dkim1 = domain_meta['domain']['dkim1']['host']
        mailbox.dns_dkim1_data = domain_meta['domain']['dkim1']['data']
        mailbox.dns_dkim2 = domain_meta['domain']['dkim2']['host']
        mailbox.dns_dkim2_data = domain_meta['domain']['dkim2']['data']
        mailbox.dns_mail_cname = domain_meta['domain']['mail_cname']['host']
        mailbox.dns_mail_cname_data = domain_meta['domain']['mail_cname']['data']
        mailbox.sendgrid_subuser = domain_meta['username']
        mailbox.domain_id = domain_meta['domain_id']
        mailbox.is_frontapp_import = is_frontapp_import
        mailbox.frontapp_token = frontapp_token

    return JsonResponse({
        'result': 'OK',
        'name': mailbox.name,
        'is_verified': mailbox.is_verified,
        'incoming_email': incoming_mailbox_name.replace(' ', ''),
        'dns': {
            'dkim1': mailbox.dns_dkim1,
            'dkim1_data': mailbox.dns_dkim1_data,
            'dkim2': mailbox.dns_dkim2,
            'dkim2_data': mailbox.dns_dkim2_data,
            'mail_cname': mailbox.dns_mail_cname,
            'mail_cname_data': mailbox.dns_mail_cname_data
        }
    })


def user_create_mailbox(request: HttpRequest) -> JsonResponse:
    """
    Get request, check if user can create a service inbox to forward their email to
    if ok, create the mailbox, send them the box address (name) as json
    :param request:
    :return: JsonResponse
    """

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)

    if str(user) == 'AnonymousUser':
        return JsonResponse({'error': 'Not authorized'}, status=403)
    if method == 'get':
        mailbox_name = mailbox_helper.random_string_generator(20) + '@holons.me'
        return JsonResponse({'result': 'OK', 'mailbox': mailbox_name})
    if method == 'post':
        return create_mailbox_item(request, user)


def user_validate_mailbox(request: HttpRequest, mailbox_name: str) -> JsonResponse:
    mailbox = Mailbox.objects.filter(name=mailbox_name).first()
    validity_status = sendgrid_helper.validate_domain(mailbox.domain_id)
    if validity_status.get('valid', False):
        mailbox.is_verified = True
        mailbox.save()

    return JsonResponse({
        'result': 'OK',
        'mailbox': mailbox_name,
        'validity_status': validity_status
    })


def mailboxes_users(request: HttpRequest) -> JsonResponse:
    """
    √ Return list of all users with access to Emails

    :param request:
    :return:
    """

    method = request_helper.method_name(request)
    if method == 'get':
        user_list = {}
        users = User.objects.all().values('id', 'username')
        for user in users:
            user_list[user['id']] = {'id': user['id'], 'username': user['username']}
        return JsonResponse({
            'result': 'OK',
            'method': method,
            'users': user_list
        })

    if method == 'post':
        user = auth_helper.get_user(request)
        logging.info(user.username)
        return JsonResponse({
            'result': 'OK',
            'method': method,
            'users_attached': 'attached',
            'owner_user': user.username
        })


def set_email_message_status(request: HttpRequest, pk) -> JsonResponse:
    """
    Get message id from the request
    Check request type
    Get or create message status object
    If method is PATCH, set status Archived
    If method is DELETE, set status DELETED
    Save MessageStatus

    :param request:
    :param pk:
    :return:
    """

    method = request_helper.method_name(request)
    message = DjangoMailboxMessage.objects.filter(pk=pk).first()
    message_status, created = MailMessageStatus.objects.get_or_create(
        message_id=message.id,
    )
    if method == 'patch':
        message_status.is_archived = True
    if method == 'delete':
        message_status.is_deleted = True
    message_status.save()

    return JsonResponse({
        'result': 'OK',
        'method': method,
        'message': {
            'id': message.id,
        }
    })


def email_settings(request: HttpRequest) -> JsonResponse:
    """
    On Get return user's email settings
    On Post set user's email settings

    :param request:
    :return:
    """

    method = request_helper.method_name(request)
    user = auth_helper.get_user(request)
    created = False

    if method == 'get':
        mail_settings = user.mailbox_settings.all().first()
        frontapp_token = mail_settings.frontapp_token
    if method == 'post':
        data = json.loads(request.body)

        frontapp_token = data.get('frontapp_token', None)
        mail_settings, created = EmailSettings.objects.get_or_create(
            frontapp_token=frontapp_token
        )
        mail_settings.save()
        if created:
            mail_settings.users.add(user)

    return JsonResponse({
        'status': 'Ok',
        'email_settings': {
            'frontapp_token': frontapp_token,
            'created': created
        }
    })



def email_settings_fa_token(request: HttpRequest) -> JsonResponse:
    """
    On Get return user's first frontapp token from mailboxes

    :param request:
    :return:
    """

    method = request_helper.method_name(request)
    user = auth_helper.get_user(request)
    frontapp_token = ''
    if method == 'get':
        for mailbox in user.mailboxes.all():
            if mailbox.frontapp_token is not None and mailbox.frontapp_token != '':
                frontapp_token = mailbox.frontapp_token
                continue

    return JsonResponse({
        'status': 'Ok',
        'email_settings': {
            'frontapp_token': frontapp_token,
        }
    })


def check_forwarding(request: HttpRequest) -> JsonResponse:
    """
    Get user's email by technical (forwarding) address
    Send test email to the real address
    Initiate mailbox.get_mail command

    :param request:
    :return:
    """
    method = request_helper.method_name(request)
    user = auth_helper.get_user(request)
    mailbox_error = None
    if method == 'post':
        logging.info('Send test email')
        data = json.loads(request.body)
        mailbox_name = data.get('mailbox', None)
        mailbox = user.mailboxes.filter(name=mailbox_name).first()
        if mailbox is not None:
            mail_to = mailbox.incoming_email
            mail_from = 'noreply@holons.me'
            subject = 'Holons email init'
            body = 'This is an initiation email for ' + mailbox_name
            success = send_email(mail_from, mail_to, subject, body)
            if not success:
                mailbox_error = 'Mail transport error'
        else:
            user_create_mailbox(request)
            check_forwarding(request)  # @todo @fixme @think Is there a way to get rid of this recursion???
            return JsonResponse({
                'status': 'Attempt to create a mailbox and then trying to resend email',
            })
    if mailbox_error is not None:
        return JsonResponse({
            'status': 'Error',
            'error': mailbox_error
        })

    if mailbox_error is None:
        logging.info('sleep')
        time.sleep(5)  # @fixme @todo Move check email to the separate method, accessible by frontend
        django_mailbox = DjangoMailbox.objects.filter(name=mailbox.name.split('@')[0]).first()
        call_command('getmail')
        logging.info(django_mailbox.from_email)


    return JsonResponse({
        'status': 'Ok',
        'test_email_sent_to': mail_to
    })


def pause_mailbox(request: HttpRequest) -> JsonResponse:
    """
    Get mailbox name from the request
    Get user's mailbox by this name
    Pause mailbox
    """

    user_id = auth_helper.get_user(request).id
    user = User.objects.filter(pk=user_id).first()
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    mailbox_name = data.get('name', None)
    mailbox = user.mailboxes.filter(name=mailbox_name).first()
    # mailbox.is_active = False  # @todo: do we need to disable paused mailbox?
    mailbox.is_paused = True
    mailbox.save()

    return JsonResponse({
        'status': 'Ok',
    })


def reenable_mailbox(request: HttpRequest) -> JsonResponse:
    """
    Get mailbox name from the request
    Get user's mailbox by this name
    Un-pause mailbox
    """

    user_id = auth_helper.get_user(request).id
    user = User.objects.filter(pk=user_id).first()
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    mailbox_name = data.get('name', None)
    mailbox = user.mailboxes.filter(name=mailbox_name).first()
    # mailbox.is_active = True  # @todo: do we need to disable paused mailbox?
    mailbox.is_paused = False
    mailbox.save()
    return JsonResponse({
        'status': 'Ok',
    })


def move_thread(request: HttpRequest) -> JsonResponse:
    """
    Get message_id, mailbox, user_id
    Fill up SharedMailMessages model with this data

    """

    user_id = auth_helper.get_user(request).id
    user = User.objects.filter(pk=user_id).first()
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    mailbox_from = mailbox_helper.get_mailbox_by_name(data.get('mailbox_from'))
    mailbox_to = mailbox_helper.get_mailbox_by_name(data.get('mailbox_to'))
    message = DjangoMailboxMessage.objects.filter(pk=data.get('message_id')).first()

    shared_messages = SharedMailMessage.objects.create(
      assigned_to_id=user.id,
      assigned_by_id=user.id,
      mailbox_from_id=mailbox_from.id,
      mailbox_to_id=mailbox_to.id,
    )
    shared_messages.messages.add(message)

    return JsonResponse({
        'status': 'Ok',
        'message': 'move_thread',
    })


# def user_mailboxes(request: HttpRequest) -> JsonResponse:
#     """
#     List Holons users' linked/pending mailboxes
#     :return: JsonResponse
#     """
# 
#     user = auth_helper.get_user(request)
#     method = request_helper.method_name(request)
#     mailboxes = {'active': [], 'pending': []}
#     for mailbox in user.mailboxes.all():
#         django_mailbox = DjangoMailbox.objects.filter(name=mailbox.name.split('@')[0]).first()
#         messages = None
#         if django_mailbox:
#             messages = DjangoMailboxMessage.objects.filter(mailbox_id=django_mailbox.id).order_by('id')
#         if messages:
#             decoded_messages = []
#             for message in messages:
#                 message_body = message.text
#                 if message.html != '':
#                     message_body = message.html
#                 decoded_messages.extend([{
#                     'html': message_body,
#                     'from_address': message.from_address,
#                     'subject': message.subject,
#                     'message_id': message.message_id,
#                     'read': message.read,
#                     'id': message.id,
#                     'processed': message.processed,
#                     'status': message_helper.get_message_status(message.id)
#                 }])
#             mailboxes['active'].extend([{
#                 'id': mailbox.id,
#                 'name': mailbox.name,
#                 'domain': mailbox.domain,
#                 'alias': mailbox.incoming_email.split('@')[0],
#                 'incoming_email': mailbox.incoming_email,
#                 'messages': list(decoded_messages),
#                 'messages_count': len(messages),
#                 'status': mailbox.is_active,
#                 'is_verified': mailbox.is_verified,
#                 'is_paused': mailbox.is_paused,
#                 'dns': {
#                     'dkim1': mailbox.dns_dkim1,
#                     'dkim1_data': mailbox.dns_dkim1_data,
#                     'dkim2': mailbox.dns_dkim2,
#                     'dkim2_data': mailbox.dns_dkim2_data,
#                     'mail_cname': mailbox.dns_mail_cname,
#                     'mail_cname_data': mailbox.dns_mail_cname_data,
#                     'is_verified': mailbox.is_verified
#                 },
#             }])
#         else:
#             mailboxes['pending'].extend([{
#                 'id': mailbox.id,
#                 'name': mailbox.name,
#                 'domain': mailbox.domain,
#                 'alias': mailbox.incoming_email.split('@')[0],
#                 'incoming_email': mailbox.incoming_email,
#                 'dkim1': mailbox.dns_dkim1,
#                 'dkim1_data': mailbox.dns_dkim1_data,
#                 'dkim2': mailbox.dns_dkim2,
#                 'dkim2_data': mailbox.dns_dkim2_data,
#                 'mail_cname': mailbox.dns_mail_cname,
#                 'mail_cname_data': mailbox.dns_mail_cname_data,
#                 'is_verified': mailbox.is_verified,
#                 'status': mailbox.is_active,
#                 'is_paused': mailbox.is_paused,
#             }])
#     return JsonResponse({
#         'result': 'OK',
#         'method': method,
#         'key': HOLONS_MAIL_API_KEY,
#         'mailboxes': mailboxes
#     })


