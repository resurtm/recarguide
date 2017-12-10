from django.conf.urls import url

from cabinet import views

app_name = 'cabinet'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
