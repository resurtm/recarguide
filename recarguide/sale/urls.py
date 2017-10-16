from django.conf.urls import url

from recarguide.sale import views

urlpatterns = [
    url(r'^$', views.sale, name='index'),

    url(r'^step1/$', views.step1, name='step1'),
    url(r'^step2/$', views.step2, name='step2'),
    url(r'^step3/$', views.step3, name='step3'),
    url(r'^step4/$', views.step4, name='step4'),
    url(r'^step5/$', views.step5, name='step5'),

    url(r'^fetch-models/(?P<make_id>\d+)/$', views.fetch_models,
        name='fetch_models'),
    url(r'^fetch-categories/(?P<category_id>\d+)/$', views.fetch_categories,
        name='fetch_categories'),
]
