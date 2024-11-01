from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.login_view, name='login'),  # Login page
    path('billing_records/', views.billing_records, name='billing_records'),
    path('create_billing_record/', views.create_billing_record, name='create_billing_record'),
    path('process_payment/<int:record_id>/', views.process_payment, name='process_payment'),
]

