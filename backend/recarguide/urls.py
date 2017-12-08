from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('common.urls', namespace='common')),
    url(r'^admin/', admin.site.urls),
]
