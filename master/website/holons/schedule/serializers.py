from rest_framework.serializers import ModelSerializer

from ls.joyous.models import (SimpleEventPage, MultidayEventPage, RecurringEventPage,
                              MultidayRecurringEventPage, removeContentPanels)

class EventSerializer(ModelSerializer):
    class Meta:
        model = SimpleEventPage
        fields = (
            'page_ptr_id',
            'time_from',
            'time_to',
            'location',
            'details',
            'website',
            'date',
            'category_id',
            'group_page_id',
            'image_id',
            # 'tz',
            'uid',
        )
