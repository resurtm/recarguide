from django.conf.urls import url

from recarguide.cabinet import views

app_name = 'cabinet'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
