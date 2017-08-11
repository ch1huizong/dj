# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Bookmark, Link, Tag

admin.site.register(Link)
admin.site.register(Tag)

class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'link',)
    filter_horizontal = ('tags',)
    
admin.site.register(Bookmark, BookmarkAdmin)
