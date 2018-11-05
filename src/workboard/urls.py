from django.conf.urls import url
from .views import show, data_chart, data_table, create, data_bubble, update

urlpatterns = [
	url(r'^(?P<id>\d+)/$', show, name='show'),
	url(r'^create/$', create, name='create'),
	url(r'^(?P<id>\d+)/update/$', update, name='update'),
	url(r'^(?P<id>\d+)/data_chart/$', data_chart, name='chart'),
	url(r'^(?P<id>\d+)/data_bubble/$', data_bubble, name='bubble'),
	url(r'^(?P<id>\d+)/data_table/$', data_table, name='table'),
]
