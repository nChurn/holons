from django.urls import path
import email_api.views as views

# /api/mailboxes/
urlpatterns = [
    path('users', views.mailboxes_users, name='mailboxes_users'),
    # path('user_mailboxes', views.user_mailboxes, name='user_mailboxes'),
    path('user_mailboxes_list', views.user_mailboxes_list, name='user_mailboxes_list'),
    path('user_get_mailbox_messages', views.user_get_mailbox_messages, name='user_get_mailbox_messages'),
    path('user_get_all_unread_messages', views.user_get_all_unread_messages, name='user_get_all_unread_messages'),
    path('user_create_mailbox', views.create_mailbox_item, name='create_mailbox_item'),
    path('user_add_mailbox', views.user_create_mailbox, name='user_create_mailbox'),
    path('check-forwarding', views.check_forwarding, name='check_forwarding'),
    path('check_forwarding', views.check_forwarding, name='check_forwarding'),
    path('user_validate_mailbox/<str:mailbox_name>', views.user_validate_mailbox, name='user_validate_mailbox'),
    path('send_email', views.user_send_email, name='user_send_email'),
    path('message/<int:pk>', views.set_email_message_status, name='set_email_message_status'),
    path('settings', views.email_settings, name='email_settings'),
    path('settings/frontapp-token', views.email_settings_fa_token, name='email_settings_fa_token'),
    path('pause', views.pause_mailbox, name='pause_mailbox'),
    path('reenable', views.reenable_mailbox, name='reenable_mailbox'),
    path('move_thread', views.move_thread, name='move_thread'),
]
