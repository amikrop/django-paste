from django.contrib import admin

from paste.models import Snippet


@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    readonly_fields = ['owner', 'created', 'updated', 'id']
