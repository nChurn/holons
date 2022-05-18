from django.contrib import admin

from subscription.models import Subscription

# admin.site.register(Subscription)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    # fields = ('id', 'subscription_type', 'owner', 'is_active')
    # __unicode__.short_description = 'aaa'
    list_display = ('id', 'get_owner',
                    'subscription_type', 'is_active',
                    'created_at', 'expires_at', 
                  )
    filter_horizontal = ('owner',)
