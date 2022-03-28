"""Defines Url pattern for daybook"""
from django.urls import path
from . import views

app_name = 'daybook'
urlpatterns = [
    # Mane page
    path('', views.index, name='index')
]
