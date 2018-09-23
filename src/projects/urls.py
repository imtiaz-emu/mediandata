from django.conf.urls import url
from .views import show, index, update, create, destroy

urlpatterns = [
	url(r'^(?P<id>\d+)/update/$', update, name='update'),
	url(r'^(?P<id>\d+)/destroy/$', destroy, name='destroy'),
	url(r'^(?P<id>\d+)/$', show, name='show'),
	url(r'^create/$', create, name='create'),
	url(r'^$', index, name='index'),
]
