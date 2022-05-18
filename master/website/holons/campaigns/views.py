import json
import logging

from datetime import datetime, timezone, timedelta
from operator import itemgetter
from django.shortcuts import render
from django.http import HttpRequest, JsonResponse
from django.core import serializers
from email_api.helpers import auth_helper
from email_api.helpers import request_helper
from accounts.models import User
from campaigns.models import Campaign
from campaigns.models import Log as CampaignLog
from rays.models.ray_template import RayTemplate



'''
    We keep Campaigns and Templates in the same place,
    for they're in the same UI place visually
'''


def show(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    campaigns = user.campaigns
    # campaigns_data = serializers.serialize('json', user.campaigns.all())
    campaigns_data = []
    now = datetime.now(timezone.utc)
    start_time = now - timedelta(seconds=60*60*24*7)

    for campaign in campaigns.all():
        templates = []
        for template in campaign.templates.all():
            bids_this_week = template.logs\
                                      .filter(event_type='bid')\
                                      .filter(event_date__range=[start_time, now])
            replies_this_week = template.logs\
                                      .filter(event_type='reply')\
                                      .filter(event_date__range=[start_time, now])

            templates.append({
                'id': template.id,
                'title': template.title,
                'bids': template.bids_total,
                'replies': template.replies,
                'bids_this_week': len(bids_this_week),
                'replies_this_week': len(replies_this_week),
                'conversions': template.conversions,
                'is_archived': template.is_archived,
            })

        campaigns_data.append({
            'id': campaign.id,
            'title': campaign.title,
            'owner': campaign.owner.first().username,
            'beneficiary': campaign.beneficiary,
            'templates': sorted(templates, key=lambda a: a['bids'], reverse=True),
        })

    return JsonResponse({
        'result': 'Wrong method',
        'entry point': 'show campaigns',
        'campaigns': campaigns_data,
        'method': method,
    })


def create(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    title = data.get('title', 'Untitled campaign')
    # beneficiary = data.get('beneficiary', '@grintender')
    beneficiary = '@grintender'  # @todo: remove hardcoded beneficiary when ready

    campaign = Campaign.objects.create(title=title, beneficiary=beneficiary)
    campaign.owner.add(user)

    return JsonResponse({
        'result': 'New campaign created',
        'data': data,
        'entry point': 'create campaign',
        'method': method,
    })


def update(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)

    return JsonResponse({
        'result': 'Wrong method',
        'method': method,
    })


def destroy(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    # data = json.loads(request.body)

    return JsonResponse({
        'result': 'Wrong method',
        'entry point': 'destroy campaign',
        'method': method,
    })


def templates_show(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    campaigns = user.campaigns.all()

    templates = []
    for campaign in campaigns.all():
        for template in campaign.templates.all():
            if not template.is_archived:
              templates.append({
                  'id': template.id,
                  'title': template.title,
                  'bids': template.bids_total,
                  'replies': template.replies,
                  'conversions': template.conversions,
              })

    return JsonResponse({
        'result': 'Wrong method',
        'entry point': 'show templates',
        'method': method,
        'templates': sorted(templates, key=lambda a: a['title'].lower()),
    })


def templates_create(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    campaign_id = data.get('campaign', None)
    title = data.get('title', None)
    campaign = Campaign.objects.filter(pk=campaign_id).first()
    template = RayTemplate.objects.create(title=title)
    campaign.templates.add(template)

    return JsonResponse({
        'result': 'Template created',
        'entry point': 'create template',
        'method': method,
    })


def templates_update(request: HttpRequest) -> JsonResponse:

    user = auth_helper.get_user(request)
    method = request_helper.method_name(request)
    data = json.loads(request.body)
    template_id = data.get('template_id')
    scope = data.get('scope', 'bids')
    template = RayTemplate.objects.filter(pk=template_id).first()
    log_data = {}
    if 'bids' == scope:
        template.bids_total += 1
        CampaignLog.objects.create(
          event_type='bid',
          template_id=template_id,
        )
    elif 'replies' == scope:
        template.replies += 1
        CampaignLog.objects.create(
          event_type='reply',
          template_id=template_id,
        )
    template.save()


    return JsonResponse({
        'result': 'Template updated',
        'entry point': 'update template',
        'data': data,
        'method': method,
    })
