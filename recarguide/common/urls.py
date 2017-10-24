from django.conf.urls import url

from recarguide.common import views

app_name = 'common'

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
