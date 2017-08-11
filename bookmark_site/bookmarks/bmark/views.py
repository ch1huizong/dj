# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import Link, Bookmark, Tag
from .forms import RegistrationForm, BookmarkForm

def main_page(request):
    return render(request, 'bmark/main_page.html')


def user_page(request, username):
    user = get_object_or_404(User, username=username) 
    bookmarks = user.bookmark_set.order_by("-id") 
    return render(request, 'bmark/user_page.html',
                 {'username': username,
                  'bookmarks': bookmarks,
                  'show_tags': True})

def tag_page(request, tagname):
    tag = get_object_or_404(Tag, name=tagname) 
    bookmarks = tag.bookmark_set.order_by("-id") 
    return render(request, 'bmark/tag_page.html',
                 {'tagname': tagname,
                  'bookmarks': bookmarks,
                  'show_tags': True,
                  'show_user': True})

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email'])
            return redirect('register_success')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html',
                 {'form': form})

@login_required
def bookmark_save(request):
    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            link, dummy = Link.objects.get_or_create(url=form.cleaned_data['url'])
            bookmark, created = Bookmark.objects.get_or_create(link=link, 
                                user=request.user)
            bookmark.title = form.cleaned_data['title']

            if not created:
                bookmark.tags.clear()
            tag_names = form.cleaned_data['tags'].split()
            for tag_name in tag_names:
                tag, dummy = Tag.objects.get_or_create(name=tag_name)
                bookmark.tags.add(tag)
            bookmark.save()
            return redirect('user_page', request.user.username)
    else:
        form = BookmarkForm()
    return render(request, 'bmark/bookmark_create.html', 
                {'form': form})
