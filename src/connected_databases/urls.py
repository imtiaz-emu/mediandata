from django.conf.urls import url
from .views import connect, create_csv

urlpatterns = [
	url(r'^connect/$', connect, name='connect'),
	url(r'^create/$', create_csv, name='create'),
]
