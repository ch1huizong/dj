# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Link(models.Model):
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.url

class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __unicode__(self):
        return self.name

class Bookmark(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.link.url)

