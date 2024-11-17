from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/edit/', views.doctor_update, name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('medical-tests/', views.medical_test_management, name='medical_test_management'),
    path('medical-tests/create/', views.medical_test_create, name='medical_test_create'),
    path('medical-tests/<int:test_id>/edit/', views.medical_test_update, name='medical_test_update'),
    path('medical-tests/<int:test_id>/delete/', views.medical_test_delete, name='medical_test_delete'),
    path('consultations/book/', views.book_consultation, name='book_consultation'),
    path('consultations/', views.consultation_list, name='consultation_list'),
]