#profileandbilling/urls.py

from django.urls import path
from . import views
from .views import patient_billing_records, logout_view


urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.login_view, name='login'),  # Login page
    path('billing_records/', views.billing_records, name='billing_records'),
    path('create_billing_record/', views.create_billing_record, name='create_billing_record'),
    path('process_payment/<int:record_id>/', views.process_payment, name='process_payment'),
    path('patient-billing-records/', patient_billing_records, name='patient_billing_records'),
    path('patients/', views.list_patients, name='list_patients'),  # List all patients
    path('patients/<int:patient_id>/', views.view_patient, name='view_patient'),  # View patient detail
    path('patients/<int:patient_id>/edit/', views.update_patient, name='update_patient'),  # Edit patient
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),  # Delete patient
    path('user-home/', views.user_home, name='user_home'),  # User home page
    path('logout/', logout_view, name='logout'),  # Logout page
]

