from django.shortcuts import render
from .models import Dashboard
from workboard.models import Workboard
from projects.models import Project
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
	project = Project.objects.get(id=request.POST.get('project_id'))
	dashboard = project.dashboard_set.create(
		name='New Dashboard'
	)
	return redirect('dashboard:show', id=dashboard.pk)


def update(request, id=None):
	pass


def destroy(request, id=None):
	pass