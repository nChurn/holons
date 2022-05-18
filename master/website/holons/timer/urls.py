""" api/timer/
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import DetailView
import timer.views as views

urlpatterns = [
    path('', views.timer_page, name='timer_index'),
    path('start', views.tm_start, name='timer_start'),
    path('stop', views.tm_stop, name='timer_stop'),
    path('cancel', views.tm_cancel, name='timer_cancel'),
    path('work-periods', views.tm_info, name='get timer'),
    path('current-status/', views.tm_current_status, name='current_status'),  # :todo: this slash is ugly 
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
