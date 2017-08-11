from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from registration.backends.simple.views import RegistrationView

class MyRegistrationView(RegistrationView):
    success_url = '/rango/add_profile/'


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^rango/', include('rango.urls')),
    url(r'^accounts/register/$', MyRegistrationView.as_view(),  name='registration_register'),
    url(r'^accounts/', include('registration.backends.simple.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
