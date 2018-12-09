from django.shortcuts import render
from .models import Dashboard
from workboard.models import Workboard
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def show(request, id=None):
	dashboard = get_object_or_404(Dashboard, id=id)
	workboards = Workboard.objects.filter(project=dashboard.project)
	dashboards = Dashboard.objects.filter(project=dashboard.project)
	context = {
		'dashboard': dashboard,
		'dashboards': dashboards,
		'workboards': workboards,
	}
	return render(request, "dashboards/show.html", context)


def create(request):
	pass


def update(request, id=None):
	pass


def destroy(request, id=None):
	pass