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
        ('draft', '草稿'),
        ('published', '已发布'),
    )
    title = models.CharField('标题',max_length=250)
    author = models.ForeignKey(User, related_name="blog_posts",
                                verbose_name='作者')
    body = models.TextField('内容')
    publish = models.DateTimeField('发布日期',default=timezone.now)
    created = models.DateTimeField('创建日期',auto_now_add=True)
    updated = models.DateTimeField('更新日期',auto_now=True)
    status = models.CharField('状态',max_length=10,
                            choices=STATUS_CHOICES, default="draft")
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        ordering = [ '-publish', ]

    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                        args=[self.id])


    def __unicode__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField('姓名',max_length=80)
    email = models.EmailField('邮件')
    body = models.TextField('内容')
    created = models.DateTimeField('创建日期',auto_now_add=True)
    updated = models.DateTimeField('更新日期',auto_now=True)
    active = models.BooleanField('活跃',default=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return '{} 评论 {}'.format(self.name, self.post)
