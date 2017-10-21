from django.conf.urls import url

from recarguide.common import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
]
