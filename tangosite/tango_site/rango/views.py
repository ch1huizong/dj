#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required 

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from bing_search import run_query  # 可以？??

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list,
                    'pages': page_list}
    
    visits = request.session.get('visits', 1) 

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    
    # 判断是否设置了session
    if last_visit: 
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 5:
            reset_last_visit_time = True
            visits = visits + 1
    else:
        reset_last_visit_time = True

    # 实际设置session
    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits 

    response = render(request, 'rango/index.html', context_dict)

    return response

def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    context_dict['category_name'] = category_name_slug
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    if request.method == 'POST': # 服务器状态
        query = request.POST['query'].strip() 
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list
            context_dict['query'] = query 
    if not context_dict['query']:
            context_dict['query'] = category.name # bug?

    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    # url得到的slug和传递的上下文变量
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)  # false
                page.category = cat  # need
                page.views = 0
                page.save()
                return category(request,category_name_slug) # 重定向需要提供目录url
        else:
            print form.errors
    else:
        form = PageForm()

    context_dict = {'form': form, 'category':cat} # 注意传递的上下文变量
    return render(request, 'rango/add_page.html', context_dict)

@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}

    if request.method == 'GET':
        cat_id = request.GET['category_id']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=cat_id)
            p = Page.objects.get_or_create(category=category, url=url, title=title)

            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages'] = pages
    return render(request, 'rango/page_list.html', context_dict)

@login_required
def like_category(request):
    cat_id = None
    likes = 0

    if request.method == 'GET':
        cat_id = request.GET['category_id']
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)

#helper
def get_category_list(max_results=0, startswith=''):
    cat_list = []
    if startswith:
        cat_list = Category.objects.filter(name__istartswith=startswith)
        if cat_list and max_results > 0:
            if cat_list.count() > max_results:
                cat_list = cat_list[:max_results]
    return cat_list

def suggest_category(request):
    cat_list = []
    startswith = ''
    if request.method == 'GET':
        startswith = request.GET['suggestion']

    cat_list = get_category_list(8, startswith)
    return render(request, 'rango/cats.html', {'cats': cat_list})

def about(request):
    if request.session.get('visits'): #使用了session cookie
        count = request.session.get('visits')
    else:
        count = 0
        
    return render(request, 'rango/about.html', {'visits': count})

# 自己定义注册、登录、登出
def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) # hash
            user.save()
            
            # commit=false最主要的是延迟保存
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()  #save

            registered = True  #set，告诉模板注册成功
        else:
            print user_form.errors, profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)  #告诉Django持久性会话
                return HttpResponseRedirect('/rango/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "rango/login.html", {})

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def user_logout(request):
    logout(request)  # 结束本次会话

    return HttpResponseRedirect('/rango/')

# track page
def track_url(request):  # 只从request中的得到信息
    page_id = None       # 可以不设置吧
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass
    return redirect(url)

#自定义profile
def register_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()  #save
            return HttpResponseRedirect(reverse('index'))
        else:
            print profile_form.errors
    return render(request, 'registration/profile_registration.html',{})
