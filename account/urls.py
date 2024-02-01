from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from account import views

urlpatterns = [
    path('account/register/', views.RegisterView.as_view()),
    path('account/token/', views.LoginView.as_view()),

]