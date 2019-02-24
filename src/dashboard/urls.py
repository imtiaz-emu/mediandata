from django.conf.urls import url
from .views import show, create, destroy, update, update_name, data_bubble, data_chart, data_table

urlpatterns = [
    url(r'^(?P<id>\d+)/$', show, name='show'),
    url(r'^create/$', create, name='create'),
    url(r'^(?P<id>\d+)/destroy/$', destroy, name='destroy'),
    url(r'^(?P<id>\d+)/update/$', update, name='update'),
    url(r'^(?P<id>\d+)/update_name/$', update_name, name='update_name'),
    url(r'^(?P<id>\d+)/data_chart/$', data_chart, name='chart'),
    url(r'^(?P<id>\d+)/data_bubble/$', data_bubble, name='bubble'),
    url(r'^(?P<id>\d+)/data_table/$', data_table, name='table'),
]
