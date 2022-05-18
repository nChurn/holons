from django.urls import path
import relations.views as views
import relations.offers as offers
import relations.commitments as commitments
import relations.invoices as invoices

# /api/relations/
urlpatterns = [
    path('', views.relations_index, name='relations_index'),
    path('offers', offers.index, name='relations_offers'),
    path('offers/create', offers.create, name='relations_offers_create'),
    path('offers/<str:invite_token>', offers.get_by_token, name='relations_get_offer_by_token'),
    path('offers/<str:pk>/delete', offers.delete, name='relations_offers_delete'),
    path('offers/<str:pk>/edit/', offers.edit, name='relations_offers_edit'),
    path('offers/<str:pk>/accept/', offers.accept, name='relations_offers_accept'),
    path('offer/<str:pk>', offers.show, name='relations_single_offer'),
    # @todo: make all urls look like offers/...
    path('commitments', commitments.index, name='relations_commitments'),
    path('invoices', invoices.index, name='relations_invoices'),
    path('invoices/create', invoices.create, name='relations_invoices_create'),
    path('invoices/<str:pk>', invoices.show, name='relations_invoices_show'),
    path('invoices/<str:pk>/accept/', invoices.accept, name='relations_invoices_accept'),
]
