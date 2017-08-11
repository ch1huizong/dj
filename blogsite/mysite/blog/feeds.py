# -*- coding:UTF-8 -*-

from django.contrib.syndication.views import Feed
from django.template.defaultfilters import slice_filter
from .models import Post

class LatestPostsFeed(Feed):
    title = '我的博客'
    link = '/blog/'
    description = '我的博客的最新文章'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return slice_filter(item.body, "30")


