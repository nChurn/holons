import logging

from django.core.management.base import BaseCommand

from accounts.models import User
from django_mailbox.models import Mailbox as DjangoMailbox
from django_mailbox.models import Message as DjangoMailboxMessage

from django.conf import settings


class Command(BaseCommand):
    help = 'Check email for a single mailbox (for use in debugging)'
    MAILBOX_NAME = '1sv4r5nuv8kwwimk2ss6'

    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs
        Get all new mail for the MAILBOX_NAME

        :param args:
        :param options:
        :return:
        """

        logging.info('I am Get single mailbox Mail command v. 1.0')
        mailbox = DjangoMailbox.objects.filter(name=self.MAILBOX_NAME).first()
        logging.info('Getting mail for mailbox.id: ' + str(mailbox.id))
        new_mail = mailbox.get_new_mail()
        for message in new_mail:
            logging.info(
                'Received %s (from %s)',
                message.subject,
                message.from_address
            )

