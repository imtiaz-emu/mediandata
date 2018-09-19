from django.conf.urls import url
from .views import show, edit, update

urlpatterns = [
	url(r'^(?P<id>\d+)/update/$', update, name='update'),
	url(r'^(?P<id>\d+)/$', show, name='show'),
	url(r'^(?P<id>\d+)/edit/$', edit, name='edit'),
]
