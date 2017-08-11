# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset()\
                    .filter(status="published")

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date="publish")
    author = models.ForeignKey(User, related_name="blog_posts")
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                            choices=STATUS_CHOICES, default="draft")
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = [ '-publish', ]

    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                        args=[ self.publish.year,
                               self.publish.strftime('%m'),
                               self.publish.strftime('%d'),
                               self.slug])


    def __unicode__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
