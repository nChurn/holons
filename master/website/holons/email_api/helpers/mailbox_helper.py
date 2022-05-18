import string
import json
import random
import requests
import logging

from . import sendgrid_helper
from django.conf import settings
from email_api.models import Mailbox
from django_mailbox.models import Mailbox as DjangoMailbox


HOLONS_MAIL_API_KEY = settings.MODOBOA_MAIL_API_KEY
MODOBOA_MAIL_API_URL = settings.MODOBOA_MAIL_API_URL
AUTH_HEADERS = {'Content-type': 'application/json', 'Authorization': 'Token ' + HOLONS_MAIL_API_KEY}


def get_mailbox_by_name(name: str) -> Mailbox:
    return Mailbox.objects.filter(name=name).first()

def random_string_generator(size: int = 20, chars: str = (string.ascii_lowercase + string.digits)) -> str:
    """
    Return a string of mixed letters/numbers of given length

    :param size:
    :param chars:
    :return:
    """
    return ''.join(random.choice(chars) for _ in range(size))


def account_create_password(username: str) -> str:
    """
    Take email username, generate password based on it

    :param username:
    :return:
    """
    password = 'holons_redirect_password_' + username + '_A_11'  # @todo: add salt, maybe?
    return password


def account_exists(mailbox_fullname: str) -> bool:
    """
    Check if email account physically exists on production server

    :param mailbox_fullname:
    :return: Boolean
    """
    url = MODOBOA_MAIL_API_URL + "accounts/exists/?email=" + mailbox_fullname
    response = requests.get(url, headers=AUTH_HEADERS)
    logging.info(url)
    logging.info(response.json())
    return response.json()['exists']


def account_create(mailbox_fullname: str) -> dict:
    """
    Create new email account on production server

    :param mailbox_fullname:
    :return: Boolean
    """
    url = MODOBOA_MAIL_API_URL + "accounts" + '/'  # + mailbox_fullname + '/'
    username = mailbox_fullname.split('@')[0]
    domain = mailbox_fullname.split('@')[1]
    password = account_create_password(username)

    data = {
        "username": mailbox_fullname,
        "first_name": "",
        "last_name": "",
        "is_active": "true",
        "role": "SimpleUsers",
        "mailbox": {
            "full_address": mailbox_fullname,
            "use_domain_quota": "true",
            "quota": "50"
        },
        "phone_number": "",
        "domains": [
            domain
        ],
        "password": password,
        "random_password": "false"
    }
    response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data))
    logging.info(response.json())
    return response.json()


def account_create_incoming_domain(incoming_email: str) -> str:
    """
    Parse email string, return domain part
    :param incoming_email:
    :return:
    """
    return incoming_email.split('@')[1]


# @todo: Check if this thing is used anywhere in the code
def set_mailbox_status(mailbox, messages):
    logging.info('check mailbox status')
    for message in messages:
        message_body = re.sub('<[^<]+?>', '', message.html)
        if message_body == 'This is an initiation email for ' + mailbox.name:
            mailbox.is_active = True
            mailbox.save()
    pass


def user_create_django_mailbox(mailbox_name):
    """
    Create Django Email credentials record to access user's mailbox
    :param mailbox_name:
    :return:
    """
    mailbox_username = mailbox_name.split('@')[0]
    mailbox_domain = mailbox_name.split('@')[1]
    mailbox_password = mailbox_helper.account_create_password(mailbox_username)
    uri = 'imap+tls://' + mailbox_username + '%40' + mailbox_domain + ':' + mailbox_password + '@' + mailbox_domain
    DjangoMailbox.objects.create(
        name=mailbox_username,
        uri=uri,
        from_email=mailbox_name,
        active=True
    )


def user_mailbox_confirm_use(domain: str, mailbox_name: str) -> dict:
    """
    Get user's mailbox, send requests to the SendGrid domain API,
        — add SubUser to the SendGrid
        — add Domain to the SendGrid
        — get domain-id
        — link Domain to the SendGrid SubUser by the domain-id
        — link Sendgrid domain with SendGrid IP by the domain-id
        — get Domain meta-data from SendGrid API response
        — save domain_id, dns_dkim1, dns_dkim2, dns_mail_cname, sendgrid_subuser to the Mailbox model

    :param domain:
    :param dict:
    :return:
    """

    # @todo: Set exceptions here or inside each of the helper function so that we do not run into API errors
    user = sendgrid_helper.get_subuser()
    domain = sendgrid_helper.add_domain(domain)
    domain_id = domain['id']

    return {
        'result': 'OK',
        'domain_id': domain_id,
        'user_id': domain.get('user_id'),
        'username': domain.get('username'),
        'domain': domain.get('dns')
    }


