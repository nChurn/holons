from django.urls import path
from .views import KeyResultAPI, PurposeAPI, ObjectiveAPI,  contexts, key_results_types

# /api/purpose/
urlpatterns = [
    path('', PurposeAPI.as_view(), name='purposes'),
    path('<int:id>', PurposeAPI.as_view(), name='purpose'),
    path('objectives/', ObjectiveAPI.as_view(), name='objectives'),
    path('objectives/<int:id>', ObjectiveAPI.as_view(), name='objective'),
    path('keyresults/', KeyResultAPI.as_view(), name='keyresults'),
    path('keyresults/<int:id>', KeyResultAPI.as_view(), name='keyresults'),
    path('keyresults/types', key_results_types, name='keyresults_types'),
    path('contexts/', contexts, name='contexts'),
]
