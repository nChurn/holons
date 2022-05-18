from django.urls import path
import campaigns.views as views

urlpatterns = [
    path('templates', views.templates_show, name='templates_show'),
    path('templates/create', views.templates_create, name='templates_create'),
    path('templates/update', views.templates_update, name='templates_update'),
    path('show', views.show, name='show'),
    path('show/<pk>', views.show, name='show'),
    path('create', views.create, name='create'),
    path('update', views.update, name='update'),
    path('update/<pk>', views.update, name='update'),
    path('delete/<pk>', views.destroy, name='destroy'),
]
