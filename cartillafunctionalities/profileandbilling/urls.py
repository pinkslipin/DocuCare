from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.login_view, name='login'),  # Login page
]
