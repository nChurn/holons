from django.urls import path
import rays.views as views
import rays.direct_messages as direct_messages
import rays.routes_automation as routes_automation

"""
/api/rays/
"""

urlpatterns = [
    path('', views.user_rays, name='user_rays'),
    path('search', views.search, name='search'),
    path('message/add', direct_messages.rays_custom_message, name='rays_custom_message'),
    path('message/<pk>', views.rays_message, name='rays_message'),
    path('users', views.rays_users, name='rays_users'),
    #  @todo: there's a need for refactoring to split requests from 
    #  /api/rays to /api/plato
    #  but now we're going to create /api/rays/direct endpoints
    path('direct', direct_messages.user_rays_direct, name='user_rays'),
    path('direct/send/', direct_messages.rays_send_direct_message, name='rays_send_direct_message'),
    path('direct/status', views.user_rays_status, name='user_rays_status'),
    path('direct/message', direct_messages.rays_send_direct_message, name='rays_send_message'),
    path('direct/thread/<int:thread_id>/delete', direct_messages.rays_thread_delete, name='rays_thread_delete'),
    path('direct/thread/<int:thread_id>/archive', direct_messages.rays_thread_archive, name='rays_thread_archive'),
    path('routes/', routes_automation.list_all, name='routes_automation_list_all'),
    path('routes/reply', routes_automation.create_message, name='routes_automation_create_message'),
    path('routes/create', routes_automation.create, name='routes_automation_create'),
    path('routes/update', routes_automation.update, name='routes_automation_update'),
    path('routes/delete/<int:item_id>/', routes_automation.destroy, name='routes_automation_destroy'),
    path('<pk>', views.save_ray_settings, name='save_ray_settings'),
]
