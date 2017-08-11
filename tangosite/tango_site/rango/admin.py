# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Category, Page, UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')

admin.site.register(Page, PageAdmin)

admin.site.register(UserProfile)


