from django.urls import path

from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),

    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail,
        name='post_detail',
    ),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),

    #path('', views.PostListView.as_view(), name='post_list'),
    #path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
