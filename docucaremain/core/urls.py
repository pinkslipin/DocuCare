from django.urls import path
from . import views
from .views import PrescriptionListView, PrescriptionCreateView, PrescriptionUpdateView, PrescriptionDeleteView

urlpatterns = [
    # General Routes
    path('', views.home, name='home'),  # General Home Page
    path('landing/', views.landing_page, name='landing_page'),  # Landing Page
    path('register/patient/', views.register_patient, name='register_patient'),
    path('register/doctor/', views.register_doctor, name='register_doctor'),
    path('login/', views.login_view, name='login'),  # Login
    path('logout/', views.logout_view, name='logout'),  # Logout

    # Admin-Specific Routes
    path('admin-home/', views.admin_home, name='admin_home'),  # Admin Home
    path('doctors/<int:pk>/', views.view_doctor, name='view_doctor'),  # View Doctor Details
    path('doctors/', views.doctor_list, name='doctor_list'),  # List of Doctors
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor_update'),  # Edit Doctor
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),  # Delete Doctor
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # Admin Profile
    path('medical-tests/', views.medical_test_management, name='medical_test_management'),  # Manage Medical Tests
    path('medical-tests/create/', views.medical_test_create, name='medical_test_create'),  # Create Medical Test
    path('medical-tests/<int:test_id>/edit/', views.medical_test_update, name='medical_test_update'),  # Edit Medical Test
    path('medical-tests/<int:test_id>/delete/', views.medical_test_delete, name='medical_test_delete'),  # Delete Medical Test
    path('consultations/', views.consultation_list, name='consultation_list'),  # List Consultations
    path('consultations/book/', views.book_consultation, name='book_consultation'),  # Book Consultation
    path('select_consultation/', views.select_consultation, name='select_consultation'),
    path('book_consultation/<int:doctor_id>/<str:time>/', views.book_consultation, name='book_consultation'),
    path('view-medical-test-applications/', views.view_medical_test_applications, name='view_medical_test_applications'),
    path('consultations/<int:consultation_id>/add_notes/', views.add_notes, name='add_notes'),

    # User-Specific Routes
    path('user-home/', views.user_home, name='user_home'),  # User Home
    path('profile/', views.view_own_profile, name='view_own_profile'),  # User Profile
    path('profile/edit/', views.edit_own_profile, name='edit_own_profile'),  # Edit Own Profile
    path('patient-billing-records/', views.patient_billing_records, name='patient_billing_records'),  # Billing Records
    path('create-billing-record/', views.create_billing_record, name='create_billing_record'),  # Create Billing Record
    path('process-payment/<int:record_id>/', views.process_payment, name='process_payment'),  # Process Payment
    path('billing-records/', views.billing_records, name='billing_records'),  # Billing Records
    path('billing-records/delete/<int:record_id>/', views.delete_billing_record, name='delete_billing_record'),  # Delete Billing Record
    path('apply-medical-test/', views.apply_medical_test, name='apply_medical_test'),
    path('view-medical-test-applications/', views.view_medical_test_applications, name='view_medical_test_applications'),
    path('consultation/success/', views.consultation_success, name='consultation_success'),
    path('consultation/view/', views.view_consultations, name='view_consultations'),
    path('doctor/profile/', views.view_own_doctor_profile, name='view_own_doctor_profile'),
    # Patient Management (Admin-Specific)
    path('patients/', views.list_patients, name='list_patients'),  # List Patients
    path('patients/<int:patient_id>/', views.view_patient, name='view_patient'),  # View Patient Details
    path('patients/<int:patient_id>/edit/', views.update_patient, name='update_patient'),  # Edit Patient
    path('patients/<int:patient_id>/delete/', views.delete_patient, name='delete_patient'),  # Delete Patient
    path('patients/<int:patient_id>/cancel/', views.cancel_update_patient, name='cancel_update_patient'),  # Cancel Patient Update

    # Prescription Routes
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription_list'),
    path('prescriptions/new/', PrescriptionCreateView.as_view(), name='prescription_create'),
    path('prescriptions/<int:pk>/edit/', PrescriptionUpdateView.as_view(), name='prescription_update'),
    path('prescriptions/<int:pk>/delete/', PrescriptionDeleteView.as_view(), name='prescription_delete'),
    path('view-prescriptions/', views.view_prescriptions, name='view_prescriptions'),
]
