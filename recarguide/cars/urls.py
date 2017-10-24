from django.conf.urls import url

from recarguide.cars import views

app_name = 'cars'

urlpatterns = [
    url(r'^(?P<slug>[0-9a-z_-]+)-(?P<id>\d+)/$', views.view, name='view'),
]
