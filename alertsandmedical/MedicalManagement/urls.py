from django.urls import path
from .views import PrescriptionListView, PrescriptionCreateView

app_name = 'medical'

urlpatterns = [
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/new/', PrescriptionCreateView.as_view(), name='prescription_create'),  # New path for adding a prescription
]