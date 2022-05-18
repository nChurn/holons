import logging
import json
import random
import datetime

from accounts.models import User
from timer.models import UserInfo
from timer.models import WorkPeriod
from relations.models import Offer
from moneta.models import BusinessEntity
from django.utils import timezone


def user_timer_start(user_id: int) -> str:
    """Go to the database, ask for WorkPeriod matching given user_id
    if no such object, create it, set current time and return corresponding message as a string
    
    :todo: sims a hell simplifiable
    """

    # We got to load User by the hashed ID
    user = User.objects.get(pk=user_id)
    wp = WorkPeriod.objects.filter(user_id__exact=user.id.id)\
        .order_by('id')\
        .last()
    if wp is None or wp.timer_stop is not None:
        give = WorkPeriod(user_id=user.id.id)
        give.timer_start = timezone.now()
        give.save()
        return f'Timer for user {user.id} started'
    else:
        return f'Timer for user {user.id} running already'


def user_timer_stop(user_id: int, data: dict) -> dict:
    """Check if given user has a running timer,
    Append BusinessEntity and Commitment ids to the Timer
    Stop the timer if it's running.
    :return: dict: {result, message, status}
    """
    
    comment = data.get('comment', '')
    is_billable = data.get('is_billable', False)
    user = User.objects.get(pk=user_id)
    wp = WorkPeriod.objects.filter(user_id__exact=user.id.id).last()
    if not wp:
      return {
        'result': 'error',
        'message': f'No timer for {user.id}',
        'status': 404
      }, 
    if wp.timer_stop is None:
        wp.timer_stop = timezone.now()
        days = wp.timer_stop.day-wp.timer_start.day
        hours = wp.timer_stop.hour-wp.timer_start.hour
        minutes = wp.timer_stop.minute-wp.timer_start.minute
        seconds = wp.timer_stop.second-wp.timer_start.second
        wp.duration = days*86400+hours*3600+minutes*60+seconds
        wp.is_billable = is_billable
        wp.comment = comment
        business_entity_id = data.get('business_entity', None)
        if business_entity_id is not None:
            wp.business_entity = BusinessEntity\
                .objects\
                .get(pk=business_entity_id)
        commitment_id = data.get('commitment', None)
        if commitment_id is not None:
            wp.commitment = Offer.objects.get(pk=commitment_id)
        wp.save()
        give = UserInfo(user_id=user.id.id)
        give.worked_hours = wp.duration
        give.save()
    else:
      return {
        'result': 'error',
        'message': f'Timer stopped already for user {user.id}',
        'status': 204
      }

    return {
      'result': 'Ok',
      'message': f'Timer stopped for user {user.id}',
      'status': 200
    } 


def user_timer_cancel(user_id: int) -> dict:
    """Destroy given timer"""

    user = User.objects.get(pk=user_id)
    wp = WorkPeriod.objects.filter(user_id__exact=user_id).last()
    if not wp:
      return {
        'result': 'error',
        'message': f'No timer for {user.id}',
        'status': 404
      }, 
    wp.delete()
    return {
      'result': 'Ok',
      'message': f'Timer-entry canceled (deleted) for user {user.id}',
      'status': 200
    }


def user_get_all_time_periods(user_id: int) -> list:
    """Return all WorkPeriods for a given user"""

    users_work_periods = WorkPeriod.objects.filter(user_id=user_id)\
        .exclude(duration__isnull=True)\
        .exclude(duration=0)\
        .order_by("-timer_start")
    result = []
    for wp in users_work_periods:
        duration = f'{str(wp.duration // 3600).zfill(2)}' 
        duration += f':{str((wp.duration // 60) % 60).zfill(2)}' 
        result.append(
            {
              'id': wp.pk,
              'business_entity': wp.business_entity_title,
              'commitment_title': wp.commitment_title,
              'duration': duration,
              'timer_start': f'{wp.timer_start.strftime("%H:%M:%S %d.%m.%Y")}',
              'timer_stop': f'{wp.timer_stop.strftime("%H:%M:%S %d.%m.%Y")}',
              'comment': wp.comment,
              'is_billable': wp.is_billable,
            }
        )
    return result


def user_timer_update(user_id: int, data: dict) -> bool:
    """Add details to the timer"""

    give = UserInfo.objects.filter(user_id__exact=user_id).last()
    give.paid_hours=data.get('ph')
    give.rate=data.get('rate')
    give.save()


def user_timer_currentstatus(user_id: int) -> dict:
    time_spent_current_task = 0
    time_spent_today_total = 0
    today = timezone.now().replace(hour=0, minute=0, second=1)
    users_work_periods = WorkPeriod.objects.filter(user_id=user_id)\
        .filter(timer_start__gte=today)\
        .exclude(duration__isnull=True)\
        .exclude(duration=0)

    today_total_duration = 0
    for wp in users_work_periods:
        today_total_duration += wp.duration

    users_current_task_duration = WorkPeriod.objects.filter(user_id=user_id)\
        .filter(timer_start__gte=today)\
        .exclude(timer_stop__isnull=True)\
        .last()
    if users_current_task_duration:
        wp = users_current_task_duration
        wp.timer_stop = timezone.now()
        days = wp.timer_stop.day-wp.timer_start.day
        hours = wp.timer_stop.hour-wp.timer_start.hour
        minutes = wp.timer_stop.minute-wp.timer_start.minute
        seconds = wp.timer_stop.second-wp.timer_start.second
        current_task_duration = days*86400+hours*3600+minutes*60+seconds
        today_total_duration += current_task_duration

    ttd = today_total_duration
    ctd = current_task_duration
    time_spent_current_task = f'{str(ctd // 3600).zfill(2)}' 
    time_spent_current_task += f':{str((ctd // 60) % 60).zfill(2)}' 

    time_spent_today_total = f'{str(ttd // 3600).zfill(2)}' 
    time_spent_today_total += f':{str((ttd // 60) % 60).zfill(2)}' 

    return {
        'time_spent_current_task': time_spent_current_task,
        'time_spent_today_total': time_spent_today_total
    }

