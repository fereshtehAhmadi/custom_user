from django.urls import path
from rest_framework import routers
from accounts import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
]
