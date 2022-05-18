from django.conf import settings
from django.urls import path

from social import views

# /api/social/
urlpatterns = [
    path('address-book/', views.address_book, name='social_list_all'),
]

