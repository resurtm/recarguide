from django.conf.urls import url

from recarguide.sale import views

urlpatterns = [
    url(r'^$', views.sale, name='index'),
    url(r'^step1/$', views.step1, name='step1'),
]
