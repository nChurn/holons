"""HOLONS url configuration
  :todo: fix bloody trailing slashes
"""

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.urls import re_path

from helpers.slug_helper import view_by_slug
from schedule.api import api_router
from subscription import views as subscription

import accounts.profile_public as pb_view
import holons.views as views
import relations.invoices as invoices
import relations.offers as offers
import relations.views as relations_views
import timer.views as timer_views


urlpatterns = [
    path('', views.index, name='index'),
    path('cors-data', views.cors_data, name='cors_data'),
    path('email', views.email, name='email'),
    path('rays', views.rays, name='rays'),
    path('platos-flywheel', views.platos_flywheel, name='platos_flywheel'),
    path('workspaces', views.workspaces, name='workspaces'),
    path('relations', views.relations, name='relations'),
    path('relations/offers', views.relations, name='relations_offers'),
    # path('relations/offers/<str:invite_token>', offers.render, name='render_offer'),
    path('relations/offers/<str:invite_token>', offers.show_offer, name='relations_show_offer'),
    path('relations/commitments', views.relations, name='relations_commitments'),
    path('relations/invoices', views.relations, name='relations_invoices'),
    path('relations/invoices/<str:pk>', invoices.show_invoice, name='relations_show_invoice'),
    path('campaigns', views.campaigns, name='campaigns'),
    path('talent', views.rays, name='talent'),
    path('auth', views.login, name='auth'),
    path('login', views.login, name='login'),
    path('classic-login', views.classic_login, name='classic_login'),
    path('logout', views.logout_user, name='logout'),
    path('admin/', admin.site.urls),
    path('invitation/', include('invitation.urls')),
    
    path('api/accounts/', include('accounts.urls')),
    path('api/address-book/', include('social.urls')),
    path('api/mailboxes/', include('email_api.urls')),
    path('api/campaigns/', include('campaigns.urls')),
    path('api/rays/', include('rays.urls')),
    path('api/talents/', include('rays.urls')),
    path('api/moneta/', include('moneta.urls')),
    path('api/social/', include('social.urls')),
    path('api/relations/', include('relations.urls')),
    path('hs', views.health_status, name='health_status'),
    path('api/timer/', include('timer.urls')),
    path('time', timer_views.timer_page, name='timer_index'),

    path('layers', views.layers, name='layers'),
    path('layers/talent', views.layers_talent, name='layers_talent'),
    path('layers/talent/payroll', views.talent_payroll, name='talennt_payroll'),
    path('layers/sops', views.layers_sops, name='layers_sops'),
    path('layers/docs-wikis', views.docs_wikis, name='docs_wikis'),
    path('layers/assets', views.layers_assets, name='layers_assets'),
    path('layers/hosting', views.layers_hosting, name='layers_hosting'),
    path('layers/equity', views.layers_equity, name='layers_equity'),
    path('layers/audits', views.layers_audits, name='layers_audits'),
    path('layers/blackboxes', views.layers_blackboxes, name='layers_blackboxes'),
    path('layers/talent-augmentation-broker', views.layers_talent, name='layers_talent'),
    path('moneta', views.moneta, name='moneta'),
    path('moneta/coins', views.moneta_coins, name='moneta_coins'),
    path('identity', views.identity, name='identity'),
    path('broker', views.broker, name='broker'),
    path('broker/talent', views.broker_talent, name='broker_talent'),
    path('broker/pheme', views.broker_pheme, name='broker_pheme'),
    path('broker/grin-stock', views.broker_grinstock, name='broker_grinstock'),
    path('purpose/', views.purpose, name='purpose'),
    path('api/purpose/', include('purpose.urls')),
    path('subscribe', include('subscription.urls')), # :todo: that's a hack to provide for trailing slash
    path('subscribe/', include('subscription.urls')),


    path('api/schedule/', include(api_router.urls)),
    re_path(r'schedule/?$', views.schedule, name='schedule'),
    re_path(r'schedule/meet/?$', views.meet, name='meet'),
    re_path(r'booking-example/?$', views.booking_example, name='booking_example'),
    path('outreach', views.outreach, name='outreach'),
    path('xo', views.xo, name='xo'),
    path('dial', views.dial, name='dial'),
    path('digest', views.digest, name='digest'),
    path('hearsay', views.hearsay, name='hearsay'),

    path('platos-flywheel/subscription', views.platos_flywheel_subscription, name='platos_flywheel_subscription'),

    # boilerplates to be removed
    path('canned', views.canned, name='canned'),

    path('profile', pb_view.user_profile_own, name='profile_own'),
    path('profile/impersonate/<str:phone_number>', pb_view.user_impersonate, name='impersonate'),
    # path('<str:handle>', pb_view.user_profile, name='profile_public_handle'),

    #hack to displaay agenda coz of broken redirects
    path('agenda', views.agenda, name='agenda'),

    # hardcoded profile annd portfolios
    path('portfolios', views.portfolios, name='portfolios'),

    path('grintender', views.grintender, name='grintender'),
    path('grintender/deeds', views.grintender_deeds, name='grintender_deeds'),
    path('grintender/words', views.grintender_words, name='grintender_words'),

    path('grintender/deeds/azb', views.grintender_deeds_azb, name='grintender_deeds_azb'),
    path('grintender/deeds/avokado-today', views.grintender_deeds_avo, name='grintender_deeds_avo'),
    path('grintender/deeds/prime-estate', views.grintender_deeds_prime, name='grintender_deeds_prime'),
    path('grintender/deeds/carpedia', views.grintender_deeds_carpedia, name='grintender_deeds_carpedia'),
    path('grintender/deeds/tennis-running-delivery', views.grintender_deeds_tennis, name='grintender_deeds_tennis'),
    path('grintender/deeds/live-in-design', views.grintender_deeds_lid, name='grintender_deeds_lid'),
    path('grintender/deeds/king-the-monk', views.grintender_deeds_king, name='grintender_deeds_king'),
    path('grintender/deeds/plain-conversions', views.grintender_deeds_pc, name='grintender_deeds_pc'),
    path('grintender/deeds/corinth-trade-company', views.grintender_deeds_corinth, name='grintender_deeds_corinth'),
    path('grintender/deeds/grin-launcher', views.grintender_deeds_launcher, name='grintender_deeds_launcher'),
    path('grintender/deeds/oil', views.grintender_deeds_oil, name='grintender_deeds_oil'),


    # find a page by it's slug
    path('<str:slug>', view_by_slug, name='view_by_slug'),

    # start wagtail urls
    path('cms/', include(wagtailadmin_urls)),
    path('docs/', include(wagtaildocs_urls)),
    path('', include(wagtail_urls)),
    # end wagtail urls

    url(r'^scaled/', include('imagefit.urls')),


  ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
