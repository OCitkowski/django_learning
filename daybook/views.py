from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic

def index(reguest):
    ''' Mane page'''
    return render(reguest, 'daybook/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")


def topics(reguest):
    ''' topics list page'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics' : topics}
    return render(reguest, 'daybook/topics.html', context)


def topic(reguest, topic_id):
    ''' show topic single page'''
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic' : topic, 'entries':entries}
    return render(reguest, 'daybook/topic.html', context)
