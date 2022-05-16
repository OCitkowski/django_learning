from django.contrib import admin
from .models import Topic, Entry

class TopicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_added', 'owner', 'slug')
    list_display_links = ('id', 'title', 'slug')
    search_fields = ('title',)

    prepopulated_fields = {"slug": ("title",)}

class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'topic', 'date_added', 'owner', 'text', 'is_published', 'slug')
    list_display_links = ('id', 'title', 'slug')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ('is_published', 'text')

admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EntryAdmin)



