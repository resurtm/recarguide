from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^cars/', include('cars.urls', namespace='cars')),
    url(r'^sale/', include('sale.urls', namespace='sale')),
    url(r'^cabinet/', include('cabinet.urls', namespace='cabinet')),
    url(r'^', include('common.urls', namespace='common')),
    url(r'^', include('auth.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
]
