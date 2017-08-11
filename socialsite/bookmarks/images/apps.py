# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'
    verbose_name = 'Image bookmarks'

    def ready(self):
        import images.signals
