import logging
import datetime as dt

from django.db import models
from rest_framework.response import Response

from rest_framework.mixins import (ListModelMixin, CreateModelMixin, RetrieveModelMixin, 
                                  UpdateModelMixin, DestroyModelMixin)
from rest_framework.viewsets import GenericViewSet

from ls.joyous.models import (SimpleEventPage, MultidayEventPage, RecurringEventPage,
                              MultidayRecurringEventPage, removeContentPanels)
from wagtail.core.models import Page

from .serializers import EventSerializer

class EventsAPIEndpoint(GenericViewSet, 
                     CreateModelMixin,  
                     RetrieveModelMixin,
                     UpdateModelMixin,
                     ListModelMixin,
                     DestroyModelMixin):
    serializer_class = EventSerializer
    queryset = SimpleEventPage.objects.all()
    model = SimpleEventPage

    def create(self, request):
        """Hardcode Page creation for POC
        :TODO:
        This is so a hairy,
        Maybe we got to write a separate endpoint to create
        Wagtail Page, return it's id, and then call api again to connect
        Calendar event to the Wagtail Page?
        """

        calendar_root = Page.objects.get(id=3)
        joyous_event = SimpleEventPage(
            time_from=request.POST['time_from'],
            time_to=request.POST['time_to'],
            location=request.POST['location'],
            details=request.POST['details'],
            website=request.POST['website'],
            date=request.POST['date'],
        )
        now = dt.datetime.now()
        timestamp = str(dt.datetime.timestamp(now)).split('.')[0]
        logging.info( "event_" + str(dt.datetime.timestamp(now)))
        joyous_event = SimpleEventPage(owner_id = request.user.id.id,
                                       slug = 'event_' + timestamp,
                                       title = 'event_' + timestamp,
                                       time_from=request.POST['time_from'],
                                       time_to=request.POST['time_to'],
                                       location=request.POST['location'],
                                       details=request.POST['details'],
                                       website=request.POST['website'],
                                       date=request.POST['date'],
                                       )
        calendar_root.add_child(instance=joyous_event)
        return Response({"message": "event saved", "event": joyous_event.id})

