"""Defines Url pattern for daybook"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views
from daybook.views import IndexView, TopicsListView, EntryDetailView, TopicDetailView

app_name = 'daybook'
urlpatterns = [
    # Mane page
    path('', IndexView.as_view(), name='index'),
    #topics page
    # path('topics/', views.topics, name='topics'),
    path('topics/', login_required(TopicsListView.as_view()), name='topics'),
    # path('topic/<slug:topic_slug>/', views.topic, name='topic'),
    path('topic/<slug:topic_slug>/', login_required(TopicDetailView.as_view()), name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<slug:topic_slug>/', views.new_entry, name='new_entry'),
    path('edit_entry/<slug:entry_slug>/', views.edit_entry, name='edit_entry'),
    path('entry/<slug:entry_slug>/', login_required(EntryDetailView.as_view()), name='entry'),
]
