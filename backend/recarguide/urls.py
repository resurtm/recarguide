from django.conf.urls import url, include
from django.contrib import admin

from cars.views import index

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^cars/', include('cars.urls', namespace='cars')),
    url(r'^admin/', admin.site.urls),
]
