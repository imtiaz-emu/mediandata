from django.conf.urls import url
from .views import show

urlpatterns = [
	url(r'^(?P<id>\d+)/$', show, name='show'),
]
