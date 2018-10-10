from django.conf.urls import url
from .views import show, data_chart, data_table

urlpatterns = [
	url(r'^(?P<id>\d+)/$', show, name='show'),
	url(r'^(?P<id>\d+)/data_chart/$', data_chart, name='chart'),
	url(r'^(?P<id>\d+)/data_table/$', data_table, name='table'),
]
