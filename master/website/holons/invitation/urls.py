from django.urls import path
import invitation.views as views

# /invitation/
urlpatterns = [
    path('get-code', views.invitation_generate_code, name='invitation_generate_code'),
    path('generate-layers-invite',
          views.generate_layers_invite, name='generate_layers_invite'),
]
