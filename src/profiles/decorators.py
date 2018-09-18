from django.core.exceptions import PermissionDenied
from .models import Profile

def current_user_profile(function):
    def wrap(request, *args, **kwargs):
        profile = Profile.objects.get(pk=kwargs['id'])
        if profile.user == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap