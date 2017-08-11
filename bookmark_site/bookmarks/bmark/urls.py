from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from . import views 


urlpatterns = [
    url(r'^$', views.main_page, name='main_page'),
    url(r'^user/(\w+)/$', views.user_page, name='user_page'),
    url(r'^tag/([^\s]+)/$', views.tag_page, name='tag_page'),

    url(r'^login/$', auth_views.login, name='user_login'),
    url(r'^logout/$', auth_views.logout, name='user_logout'),
    url(r'^register/$', views.user_register, name='user_register'),
    url(r'^register_success/$', 
        TemplateView.as_view(template_name='registration/register_success.html'),
        name='register_success'),

    url(r'^save/$', views.bookmark_save, name='bookmark_save'),

]
