import logging
from twilio.rest import Client
from datetime import datetime, timezone

from django.core.management.base import BaseCommand
from talents.models import UpworkTalent
from health.models import Log
from django.conf import settings


class Command(BaseCommand):
    help = 'Get RaysSettings from the database, parse external RSS feed by url, save contents to the database'
    """
    """

    TWILIO_SID = settings.TWILIO_SID
    TWILIO_TOKEN = settings.TWILIO_TOKEN
    MASTER_RAY_PK = settings.MASTER_RAY_PK
    CEO_PHONE = settings.CEO_PHONE
    CTO_PHONE = settings.CTO_PHONE

    LOGGING = True


    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs

        :param args:
        :param options:
        :return:
        """

        logging.info('I am HOLONS health-check command v. 1.0')
        logging.info('I check platform status and send SMS if something is not OK')

        if not self.LOGGING:
            logging.info('HOLONS health-check logging DISABLED')
            logging.disable(logging.CRITICAL)

        self.check_rays()

    def send_sms(self, phone_to: str, message: str = ''):
        """
        Universal SMS sender

        :param phone_to:
        :param message:
        :return:
        """

        # Your Account SID from twilio.com/console
        account_sid = self.TWILIO_SID
        # Your Auth Token from twilio.com/console
        auth_token = self.TWILIO_TOKEN

        twilio_client = Client(account_sid, auth_token)
        message = twilio_client.messages.create(
            to="+" + phone_to,
            from_="+12512996861",
            body='HOLONS: ' + message
        )


    def check_rays(self):
        """
        Get freshest RayMessage imported from Upwork
        Check message pub_date < 2 hours ago
        Check health.Rays model for

        :return:
        """

        logging.info('Check Rays health')
        last_message = UpworkTalent.objects.filter(provider='upwork').order_by('-id')[0:1].first()
        now = datetime.now(timezone.utc)
        diff = now - last_message.pub_date
        time_in_seconds = 2 * 60 * 60  # 2 hours
        if diff.seconds > time_in_seconds:
            message = 'Upwork import failure'
            if self.check_log_status(time_in_seconds):
                self.send_sms(phone_to=self.CEO_PHONE, message=message)
                self.write_log('upwork_import_failure', self.CEO_PHONE, message, 'failure', True, now)
                self.send_sms(phone_to=self.CTO_PHONE, message=message)
                self.write_log('upwork_import_failure', self.CTO_PHONE, message, 'failure', True, now)

        logging.info(last_message.pub_date)


    def check_log_status(self, seconds: int):
        """
        Check last log record existence and created date

        :param seconds:
        :return:
        """

        send_sms = False
        sms_log_record = Log.objects.filter(event_type='upwork_import_failure').order_by('-id')[0:1].first()
        if sms_log_record is None:
            send_sms = True
        else:
            now = datetime.now(timezone.utc)
            diff = now - sms_log_record.check_date
            if diff.days > 0 or diff.seconds > seconds:
                send_sms = True

        return send_sms


    def write_log(self, event_type, receiver, message, status, is_sent, date):
        """
        Write a new record to the log storage

        :param event_type:
        :param receiver:
        :param message:
        :param status:
        :param is_sent:
        :param date:
        :return:
        """
        log_entry = Log.objects.create(
            event_type=event_type,
            receiver=receiver,
            status=status,
            is_sent=is_sent,
        )
        log_entry.save()
        pass

