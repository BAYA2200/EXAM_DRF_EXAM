from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from news import views

urlpatterns = [
    path('news/', views.NewsListCreateAPIView.as_view()),
    path('news/<int:pk>/', views.NewsRetrieveUpdateDestroyAPIView.as_view()),
    path('news/<int:pk>/comments/', views.CommentListCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/', views.CommentRetrieveUpdateDestroyAPIView.as_view()),
    path('status/', views.StatusListCreateAPIView.as_view()),
    path('status/<int:pk>/', views.StatusRetrieveUpdateDestroyAPIView.as_view()),
    path('news/<int:news_id>/<slug:slug>/', views.NewsStatusCreateAPIView.as_view()),
    path('news/<int:news_id>/comments/<int:pk>/<slug:slug>/', views.CommentStatusCreateAPIView.as_view()),

]