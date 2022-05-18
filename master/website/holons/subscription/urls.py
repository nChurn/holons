from django.conf import settings
from django.urls import path

import subscription.views as subscription

urlpatterns = [
    # /subscribe/
    path('', subscription.index, name='subscription_index'),
    path('all', subscription.list_subscriptions, name='subscription_list_all'),
    path('create-customer',
        subscription.create_customer, name='subscription_create_customer'
    ),
    path('create-early-adopter',
        subscription.create_early_adopter, name='subscription_create_early_adopter'
    ),
    path('create-plato-customer',
        subscription.create_plato_customer,
        name='subscription_create_plato_customer'
    ),
    path('cancel/<str:pk>',
        subscription.cancel_subscription,
        name='subscription_cancel_subscription'
    ),
    # webhooks
    path(settings.WH_COMMON,
        subscription.wh_common, name='subscription_wh_common'),
]
