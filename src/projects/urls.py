from django.conf.urls import url, include
from .views import show, index, update, create, destroy, update_board

urlpatterns = [
	url(r'^(?P<id>\d+)/update/$', update, name='update'),
	url(r'^(?P<id>\d+)/destroy/$', destroy, name='destroy'),
	url(r'^(?P<id>\d+)/$', show, name='show'),
	url(r'^create/$', create, name='create'),
	url(r'^$', index, name='index'),
	url(r'^(?P<id>\d+)/update_board/$', update_board, name='update_board'),
	url(r'^(?P<project_id>\d+)/connections/', include("connected_databases.urls", namespace='connected_databases')),
]
