from django.urls import path
import moneta.views as views
import moneta.business_entities as business_entities

# /api/moneta/
urlpatterns = [
    path('', views.moneta_index, name='moneta_index'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('business-entities', business_entities.crud, name='be_crud'),
    path('business-entities/<int:pk>', business_entities.crud, name='be_crud'),
    path('fixed-costs', views.FixedCostApi.as_view(), name='fixed-costs'),
    path('fixed-costs/<int:id>', views.FixedCostApi.as_view(), name='fixed-costs'),
    path('variable-costs', views.VariableCostApi.as_view(), name='variable-costs'),
    path('variable-costs/<int:id>', views.VariableCostApi.as_view(), name='variable-costs'),
    path('tags', views.CostTagApi.as_view(), name='tags'),
    path('tags/<int:id>', views.CostTagApi.as_view(), name='tags'),
]
