"""Defines Url pattern for daybook"""
from django.urls import path
from . import views

app_name = 'daybook'
urlpatterns = [
    # Mane page
    path('', views.index, name='index'),
    #topics page
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
]
