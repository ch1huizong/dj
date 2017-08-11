from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^account/', include('account.urls')),
    url(r'^images/', include('images.urls', namespace='images')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
