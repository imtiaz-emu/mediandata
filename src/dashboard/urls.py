from django.conf.urls import url
from .views import show, create, destroy, update

urlpatterns = [
    url(r'^(?P<id>\d+)/$', show, name='show'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>\d+)/destroy/$', destroy, name='destroy'),
    url(r'^(?P<id>\d+)/update/$', update, name='update')
]
