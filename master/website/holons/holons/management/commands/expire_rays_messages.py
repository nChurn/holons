import re
import time
import random
import logging
from datetime import datetime, timezone, timedelta

from django.contrib.messages.context_processors import messages
from django.core.management.base import BaseCommand
from django.db import connection

from accounts.models import User
from rays.models import RaySource
from rays.models import UpworkTalent
from rays.models import ClientStats

from django.conf import settings


class Command(BaseCommand):
    help = 'Get RaysSettings from the database, walk over each message\
    (excluding MASTER RAY) and check if its expired ' \
    'based on its pub_date'

    MASTER_RAY_PK = settings.MASTER_RAY_PK

    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs
        Get all RayMessage objects
        Exclude MASTER RAY
        Loop through each of them
        Call message expiration method for each message

        :param args:
        :param options:
        :return:
        """

        logging.info('I am expire_rays command v. 2.0')
        logging.info('I write results to: rays database')
        expired_count = 0
        now = datetime.now(timezone.utc)
        yesterday = now - timedelta(days=1)
        with connection.cursor() as cursor:
          cursor.execute("UPDATE rays_upworktalent SET is_archived = True " +
          "WHERE is_archived = False AND is_expired = False " +
          "AND ray_source_id != 41 AND pub_date < '{0}';".format(yesterday))
          count = cursor.rowcount
        logging.info('Date now: ' + str(now))
        logging.info('Expiration date: ' + str(yesterday))
        logging.info('Expired messages count: ' + str(count))


    def get_messages(self) -> list:
        logging.info('Get messages')
        rays_messages = UpworkTalent.objects.all() \
            .exclude(ray_source_id=self.MASTER_RAY_PK) \
            .exclude(is_proposed=True) \
            .exclude(is_expired=True) \
            .exclude(ray_source_id=41) 
        # this is the first huge ray for stats purposes
        return rays_messages


    def expire_message(self, message: UpworkTalent):
        now = datetime.now(timezone.utc)
        diff = now - message.pub_date
        day_in_seconds = 24 * 60 * 60 - 60
        expired = False
        if diff.seconds > day_in_seconds or diff.days > 1:
            message.is_expired = True
            message.save()
            expired = True

        return expired


