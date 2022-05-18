# from wagtail.api.v2.views import PagesAPIViewSet
# from wagtail.api.v2.router import WagtailAPIRouter
# 
# from .endpoints import EventsAPIEndpoint
# 
# api_router = WagtailAPIRouter('scheduleapi')
# 
# api_router.register_endpoint('pages', PagesAPIViewSet)
# api_router.register_endpoint('events', EventsAPIEndpoint)

from rest_framework.routers import DefaultRouter
from .endpoints import EventsAPIEndpoint
api_router = DefaultRouter('scheduleapi')
api_router.register('events', EventsAPIEndpoint)
