from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^cars/', include('recarguide.cars.urls', namespace='cars')),
    url(r'^sale/', include('recarguide.sale.urls', namespace='sale')),
    url(r'^', include('recarguide.common.urls', namespace='common')),
    url(r'^', include('recarguide.auth.urls', namespace='auth')),
    url(r'^admin/', admin.site.urls),
]
