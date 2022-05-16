from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required


def index(request):
    ''' Mane page'''
    return render(request, 'daybook/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

@login_required
def topics(request):
    ''' topics list page'''
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'daybook/topics.html', context)

@login_required
def topic(request, topic_slug):
    ''' show topic single page'''
    for item in request:
        print(item, topic_slug )
    topic = Topic.objects.get(slug=topic_slug)
    #
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.filter(is_published=True).order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'daybook/topic.html', context)

@login_required
def new_topic(request):
    """Add new topic"""
    if request.method != 'POST':
        #         to create new empty form
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            #  Error NOT NULL constraint failed: daybook_topic.owner_id
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()

            # form.save()
            return redirect('daybook:topics')

    context = {'form': form}
    return render(request, 'daybook/new_topic.html', context)

@login_required
def new_entry(request, topic_slug):
    """add new entry"""
    topic = Topic.objects.get(slug=topic_slug)
    if request.method != 'POST':
        form = EntryForm
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            # for item in request:

            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.owner = request.user
            new_entry.save()
            return redirect('daybook:topic', topic_slug=topic_slug)

    context = {'topic': topic, 'form': form}
    return render(request, 'daybook/new_entry.html', context)

@login_required
def edit_entry(request, entry_slug):
    """edit an existing entry."""
    # entry = Entry.objects.get(id=entry_id)
    entry = get_object_or_404(Entry, slug=entry_slug)
    topic = entry.topic
    #
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('daybook:topic', topic_slug=topic.slug)


    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'daybook/edit_entry.html', context)


