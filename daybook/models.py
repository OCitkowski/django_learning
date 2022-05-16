from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Topic(models.Model):
    """atribute for model text, date"""
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add= True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Topic, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Entry(models.Model):
    """ information for theme"""
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')
    is_published = models.BooleanField(default=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'entries'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Entry, self).save(*args, **kwargs)

    def __str__(self):
        if len(self.text) >= 50:
            return f"{self.text[:50]}..."
        else:
            return f"{self.text[:50]}"