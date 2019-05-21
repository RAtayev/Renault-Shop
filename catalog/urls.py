from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main/$', views.main, name='main'),
    url(r'^order/$', views.order, name='order'),
    url(r'^statistic/$', views.statistic, name="statistic")
]