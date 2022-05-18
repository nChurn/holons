import json
import requests
import logging

from django.conf import settings
# from .mailbox_helper import random_string_generator

SENDGRID_DOMAINS_API_KEY = settings.SENDGRID_DOMAINS_API_KEY
SENDGRID_DOMAINS_SUBUSER = settings.SENDGRID_DOMAINS_SUBUSER
SENDGRID_DOMAINS_IP = settings.SENDGRID_DOMAINS_IP

AUTH_HEADERS = {'Content-type': 'application/json', 'Authorization': 'Bearer ' + SENDGRID_DOMAINS_API_KEY}
API_URL = 'https://api.sendgrid.com/v3/whitelabel/domains'
USER_API_URL = 'https://api.sendgrid.com/v3/subusers'

"""
    This helper is our connection to the SendGrid Whitelabel Domain API    
"""


def get_subuser() -> dict:
    url = USER_API_URL + '?username=' + 'HolonsSubuser'
    response = requests.get(url, headers=AUTH_HEADERS)
    logging.info(response.json())
    return response.json()

def add_subuser(subuser_mailbox_name: str) -> dict:
    """
    Add domain to the SendGrid account, via SendGrid Whitelabel Domain API
    DISABLED !!!

    :param subuser_mailbox_name:
    :return:
    """

    logging.info('Add SubUser do the SendGrid')
    url = USER_API_URL
    data = {
      "username": subuser_mailbox_name,
      "email": subuser_mailbox_name,
      # "password": random_string_generator(20) + '_no_access',
      "ips": [
        SENDGRID_DOMAINS_IP,
      ]
    }
    logging.info('Send request to: ' + url)
    logging.info('Headers: ' + str(AUTH_HEADERS))
    response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data))
    logging.info(response.json())
    return response.json()


def add_domain(domain_name: str) -> dict:
    """
    Add domain to the SendGrid account, via SendGrid Whitelabel Domain API

    :param domain_name:
    :return:
    """

    logging.info('Add domain to the SendGrid')
    url = API_URL
    data = {
        "domain": domain_name,
        "automatic_security": True,
        "custom_spf": False
    }
    logging.info('Send request to: ' + url)
    logging.info('Headers: ' + str(AUTH_HEADERS))
    response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data))
    logging.info(response.json())
    return response.json()


def link_to_subuser(domain_id: int, username: str) -> dict:
    """
    Link Domain to the SendGrid SubUser by the domain-id

    :param domain_id:
    :param username:
    :return:
    """

    logging.info('Link domain to the SendGrid SubUser by the domain-id')
    url = API_URL + '/' + str(domain_id) + '/subuser'
    data = {
        "username": username
    }
    logging.info('Send request to: ' + url)
    logging.info('Headers: ' + str(AUTH_HEADERS))
    response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data))
    logging.info(response.json())
    return response.json()


def link_to_ip(domain_id: int, ip_address: str) -> dict:
    """
    Link Sendgrid domain with SendGrid IP by the domain-id

    :param domain_id:
    :param ip_address:
    :return:
    """

    logging.info('Link domain to the SendGrid SubUser by the domain-id')
    url = API_URL + '/' + str(domain_id) + '/ips'
    data = {
        "ip": ip_address
    }
    logging.info('Send request to: ' + url)
    logging.info('Headers: ' + str(AUTH_HEADERS))
    response = requests.post(url, headers=AUTH_HEADERS, data=json.dumps(data))
    logging.info(response.json())
    return response.json()


def validate_domain(domain_id: int) -> dict:
    """
    Get domain ID, ask SendGrid to ping it's DNS-records

    :param domain_id:
    :return:
    """

    url = API_URL + '/' + str(domain_id) + '/validate'
    response = requests.post(url, headers=AUTH_HEADERS)
    return response.json()
