import logging
import pytz
from datetime import datetime, timedelta
from .models import TalentStat

def rays():
    """
    Prepare data structure for hours Graph rendering
    It's important to structure messages count by hour and inside each hour by day of the week

    """

    utc = pytz.UTC
    now = datetime.now().replace(tzinfo=utc)

    monday = now + timedelta(days=-now.weekday())
    monday = monday.replace(hour=00, minute=00, second=1)

    week_logs = TalentStat.objects.filter(check_date__range=[monday, now])
    hours = {}
    h = 1
    while h < 24:
        i = 0
        days = []
        hours[h] = []
        while i < 7:
            hour_date = monday + timedelta(days=i)
            hour_date = hour_date.replace(hour=+h)
            if 23 != h:
                day_record = week_logs.filter(
                  check_date__range=[hour_date, hour_date.replace(hour=h+1)]
                ).first()
            else:
                day_record = week_logs.filter(
                  check_date__range=[hour_date, hour_date.replace(hour=23, minute=59)]
                ).first()
            if day_record is not None:
                days.append(day_record.messages_master)
            else:
                days.append(0)
            i += 1
        hours[h] = days
        h += 1
    return hours
