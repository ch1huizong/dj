from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^coupons/', include('coupons.urls', namespace='coupons')),
    url(r'^paypal/', include('paypal.standard.ipn.urls')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^', include('shop.urls', namespace='shop')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
