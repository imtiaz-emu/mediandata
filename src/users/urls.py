from django.conf.urls import url
from .views import login, show, create, register

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^create/$', create, name='create'),
    url(r'^login/$', login, name='login'),
    url(r'^(?P<id>\d+)/$', show, name='show'),
]