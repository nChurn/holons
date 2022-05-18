import logging
from datetime import datetime
from datetime import date
from django.utils import timezone
from datetime import timedelta

from timer.models import WorkPeriod as Timer
from moneta.models  import BusinessEntity


def timer_setter(request) -> dict:
    """Timer state for the front-end
    Check if the user is logged in
    Check if the user has active timer
    Get time spent today

    """

    timer_object = {}
    if request.user.is_authenticated:
      business_entites = BusinessEntity.objects\
          .filter(owner=request.user).all()\
          .values('id', 'name')
      business_entites= list(business_entites)

      timer_object['user'] = request.user
      timer_object['business_entites'] = business_entites

      # :todo: looks extensive, rewrite it using single function call
      if get_timer(user_id=request.user.id.id):
          timer_object['timer'] = get_timer(user_id=request.user.id)
      else:
          timer_object['timer'] = {'timer_active': False}
    else:
        timer_object['user'] = None
    return timer_object


def get_timer(user_id: int) -> dict:
    """Return active timer for the given user_id
    Return today timer numbers

    """

    timer_data = Timer.objects.filter(user_id=user_id).order_by('id').last()
    timer_last_closed = Timer.objects.filter(
        user_id=user_id, timer_stop__isnull=False,
    ).order_by('id').last()
    timer = {}
    timer['time_current'] = '00:00'
    if timer_data:
      if timer_data.timer_stop is None:
        timer['timer_active'] = True
        # :todo: this is legit but it'll give 27 hours 
        # :todo: if the user did't stop the timer yesterday
        # :todo: Shall we add current task's time to  the overall today time?
        timer['time_spent_current'] =\
            timezone.now().timestamp() - timer_data.timer_start.timestamp()
        timer['time_spent_current_hours'] =\
            str(int(timer['time_spent_current']) // 3600).zfill(2)
        timer['time_spent_current_minutes'] =\
            str((int(timer['time_spent_current']) // 60) % 60).zfill(2)
        timer['time_current'] = f'{timer["time_spent_current_hours"]}'
        timer['time_current'] += f':{timer["time_spent_current_minutes"]}'
    today = date.today()
    work_periods_today = Timer.objects.filter(
        user_id=user_id,
        timer_stop__year=today.year,
        timer_stop__month=today.month,
        timer_stop__day=today.day,
    )
    timer['time_spent_today'] = 0
    timer['time_spent_today_hours'] = 0
    timer['time_spent_today_minutes'] = 0
    for period in work_periods_today:
        timer['time_spent_today'] += period.duration
    date_object = timedelta(seconds=timer['time_spent_today'])
    timer['time_spent_today_hours'] = str(date_object.seconds // 3600).zfill(2)
    timer['time_spent_today_minutes'] = str((date_object.seconds // 60) % 60).zfill(2)
    timer['time_entry_title'] = timer_last_closed.comment if timer_last_closed else ''
    return timer


