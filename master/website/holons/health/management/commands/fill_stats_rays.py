import logging
import pytz
from datetime import datetime, timezone, timedelta

from django.core.management.base import BaseCommand
from talents.models import UpworkTalent
from health.models import TalentStat
from django.conf import settings


class Command(BaseCommand):
    help = 'Get RaysMessages from the database, count messages number imported by hour, store stats into the DB'
    """
    """

    LOGGING = True

    MASTER_RAY_PK = settings.MASTER_RAY_PK

    last_logged_global = None
    last_message_global = None
    imported_messages_total = 0


    def handle(self, *args, **options):
        """
        Call main command logic
        Write command name to the logs

        :param args:
        :param options:
        :return:
        """

        logging.info('I am HOLONS Rays Count stats command v. 1.0')
        logging.info('I count messages imported by hour and save the number to the DB')

        if not self.LOGGING:
            logging.info('HOLONS Rays Count stats logging DISABLED')
            logging.disable(logging.CRITICAL)

        fresh_messages = self.check_messages()
        if fresh_messages is True:
            self.generate_logs()


    def check_messages(self) -> bool:
        """
            Get total number of Ray messages in DB
            Get date of the last logged messages stats
            If last log date < then now
                start logs generation

        """

        fresh_messages = False
        logging.info('Start counting')
        messages_total = self.get_messages_total()
        last_message = self.get_last_message()
        logging.info('Total messages count = ' + str(messages_total))
        last_logged = self.get_last_log()
        logging.info('Last logged date: ' + str(last_logged.check_date) + ' id: ' + str(last_logged.id))

        if last_message.pub_date > last_logged.check_date:
            # logging.info(str(last_message))
            fresh_messages = True

        return fresh_messages


    def get_last_log(self) -> TalentStat:
        last_logged = TalentStat.objects.order_by('-id').first()
        self.last_logged_global = last_logged
        return last_logged


    def get_messages_total(self) -> int:
        messages_total = UpworkTalent.objects.all().count()
        self.imported_messages_total = messages_total
        return messages_total


    def get_last_message(self) -> UpworkTalent:
        last_message = UpworkTalent.objects.order_by('-id').first()
        self.last_message_global = last_message
        return last_message


    def generate_logs(self):
        """
            Get last log date
            Get messages, from the date to the week from it
            If messages count = 0, increase week counter and repeat
            For each hour count messages
                Store hourly stats to the DB

        :return:
        """

        last_log = self.last_logged_global
        last_message = self.last_message_global

        processed_messages = 0

        # get all messages published after the last log update
        utc = pytz.UTC
        now = datetime.now().replace(tzinfo=utc)

        messages_total = UpworkTalent.objects.filter(pub_date__range=[last_log.check_date, now]).count()
        prev_week = last_log.check_date
        weeks_count = 0
        while processed_messages < messages_total:
            week_span = last_log.check_date + timedelta(days=7+weeks_count)
            messages_to_log = UpworkTalent.objects.filter(pub_date__range=[prev_week, week_span])
            logging.info('week num:' + str(weeks_count/7))
            days_count = 1
            prev_day = prev_week
            while days_count < 8:
                days_span = prev_week + timedelta(days=days_count)
                hours_count = 0
                day_messages = messages_to_log.filter(pub_date__range=[prev_day, days_span])
                logging.info('\tday: ' + str(days_count) + ' day msgs: ' + str(len(day_messages)))
                prev_hour = prev_day
                while hours_count < 25:
                    master_messages = 0
                    ray_messages = 0
                    hours_span = prev_hour + timedelta(seconds=hours_count*60*60)
                    hour_messages = day_messages.filter(pub_date__range=[prev_hour, hours_span])
                    if hours_span <= now + timedelta(seconds=30*60):
                        if len(hour_messages) > 0:
                            master_messages = hour_messages.filter(ray_source_id__exact=self.MASTER_RAY_PK).count()
                            ray_messages = hour_messages.exclude(ray_source_id__exact=self.MASTER_RAY_PK).count()
                            logging.info('\t\t' + str(hours_count)
                                         + ' hour msgs: ' + str(len(hour_messages))
                                         + ' master: ' + str(master_messages)
                                         + ' ray: ' + str(ray_messages)
                                         )
                        TalentStat.objects.create(
                            messages_master=master_messages,
                            messages_rays=ray_messages,
                            check_date=prev_hour
                        )

                    hours_count += 1
                    prev_hour = hours_span

                days_count += 1
                prev_day = days_span
            processed_messages += len(messages_to_log)
            prev_week = week_span
            weeks_count += 7

        logging.info(
                'Messages total: ' + str(messages_total)
                 # + ' New messages count: ' + str(len(messages_to_log))
                 + ' Processed: ' + str(processed_messages)
        )




        pass



