from django import forms
from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']
        labels = {'title': ''}



class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'text', 'is_published']
        labels = {'title': 'title....', 'text': 'text....', 'is_published': 'is published'}

        # widgets = {'title': forms.CharField(), 'text': forms.Textarea(attrs={'cols': 200})}
