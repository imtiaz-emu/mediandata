from django.shortcuts import render
from .models import Dashboard
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def show(request, id=None):
	dashboard = get_object_or_404(Dashboard, id=id)
	context = {
		'dashboard': dashboard
	}
	return render(request, "dashboards/show.html", context)
