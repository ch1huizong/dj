# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if self.views < 0 or self.likes < 0 :
            raise ValueError("Views:%s and Likes:%s shoud be positive" % (self.views, self.likes))
        else:
            self.slug = slugify(self.name)
            super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __unicode__(self):
        return self.user.username
