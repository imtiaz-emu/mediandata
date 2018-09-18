from django.conf.urls import url
from .views import signin, register, signout

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^signin/$', signin, name='signin'),
    url(r'^signout/$', signout, name='signout'),
]