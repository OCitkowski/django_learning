from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.views.generic import TemplateView, ListView, DetailView

class IndexView(TemplateView):
    template_name = 'daybook/index.html'

class EntryDetailView(DetailView):
    model = Entry
    template_name = 'daybook/entry.html'
    context_object_name = 'entry'
    slug_url_kwarg = 'entry_slug'

    def get_queryset(self):
        return Entry.objects.filter(owner=self.request.user)

    # return get_object_or_404(Entry.objects.filter(owner=self.request.user))


# def index(request):
#     ''' Mane page'''
#     return render(request, 'daybook/index.html')
#     # return HttpResponse("Hello, world. You're at the polls index.")

class TopicsListView(ListView):

    paginate_by = 2
    model = Topic
    queryset = Topic.objects.order_by('date_added')
    template_name = 'daybook/topics.html'
    context_object_name = 'topics'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['title'] = 'All topic'
        # Add in a QuerySet of all the books
        # context['topics'] = Topic.objects.all()
        if len(Entry.objects.filter(owner=self.request.user)) == 0 :
            redirect('topics/')

        context['entries'] = Entry.objects.filter(owner=self.request.user)
        return context

    # def get_queryset(self):
    #     return Topic.objects.filter(owner=self.request.user)

# @login_required
# def topics(request):
#     ''' topics list page'''
#     topics = Topic.objects.filter(owner=request.user).order_by('date_added')
#     context = {'topics': topics}
#     return render(request, 'daybook/topics.html', context)

# @login_required
# def topic(request, topic_slug):
#     ''' show topic single page'''
#     topic = Topic.objects.get(slug=topic_slug)
#     #
#     # if topic.owner != request.user:
#     #     raise Http404
#     entries = topic.entry_set.filter(is_published=True).order_by('-date_added')
#     context = {'topic': topic, 'entries': entries}
#     return render(request, 'daybook/topic.html', context)

class TopicDetailView(DetailView):

    paginate_by = 2
    model = Topic
    template_name = 'daybook/topic.html'
    context_object_name = 'topic'
    slug_url_kwarg = 'topic_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['topic_slug']
        topic_id = Topic.objects.get(slug=self.kwargs['topic_slug']).id
        entries = Entry.objects.filter(is_published=True, topic=topic_id, owner=self.request.user).order_by('-date_added')
        context['entries'] = entries

        return context


# @login_required
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

# @login_required
def edit_entry(request, entry_slug):
    """edit an existing entry."""
    # entry = Entry.objects.get(id=entry_id)
    entry = get_object_or_404(Entry, slug=entry_slug)
    topic = entry.topic
    #
    if entry.owner != request.user:
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


