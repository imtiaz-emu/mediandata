from django.conf.urls import url
from .views import connect, create_csv

urlpatterns = [
	url(r'^connect/$', connect, name='connect'),
	url(r'^create_csv/$', create_csv, name='create_csv'),
]
