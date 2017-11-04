from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^cars/', include('recarguide.cars.urls', namespace='cars')),
    url(r'^sale/', include('recarguide.sale.urls', namespace='sale')),
    url(r'^cabinet/', include('recarguide.cabinet.urls', namespace='cabinet')),
    url(r'^', include('recarguide.common.urls', namespace='common')),
    url(r'^', include('recarguide.auth.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    old = urlpatterns
    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns = old + urlpatterns
