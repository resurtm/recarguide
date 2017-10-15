from django.conf.urls import url

from recarguide.sale import views

urlpatterns = [
    url(r'^$', views.sale, name='index'),
    url(r'^step1/$', views.step1, name='step1'),
    url(r'^step2/$', views.step2, name='step2'),
    url(r'^fetch-models/(?P<make_id>\d+)/$', views.fetch_models,
        name='fetch_models'),
]
