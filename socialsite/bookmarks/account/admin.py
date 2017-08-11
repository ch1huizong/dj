# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo',]
admin.site.register(Profile, ProfileAdmin)
