from django.urls import path
import accounts.views as views
import accounts.profile as profile

# /api/accounts
urlpatterns = [
    path('login', views.holons_login, name='login'),
    path('classic-login', views.holons_classic_login, name='classic_login'),
    path('confirmation', views.confirmation, name='confirmation'),
    # :todo: check if we need address-book here 
    # path('address-book', views.address_book, name='address_book'),
    path('edit', profile.edit, name='profile_edit'),
    path('upload', profile.picture_upload, name='profile_picture_upload'),
]
