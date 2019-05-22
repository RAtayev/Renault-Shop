from django.urls import path
from . import views
from django.conf.urls import url
import django.views
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main/$', views.main, name='main'),
    url(r'^order/$', views.order, name='order'),
    url(r'^statistic/$', views.statistic, name="statistic"),
]