from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from .models import Dashboard
from workboard.models import Workboard, SelectedVariables
from projects.models import Project
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def show(request, id=None):
    dashboard = get_object_or_404(Dashboard, id=id)
    all_workboards = Workboard.objects.filter(project=dashboard.project)
    valid_workboards = list(SelectedVariables.objects.filter(
        workboard__in=list(all_workboards.values_list('pk', flat=True))).values('workboard').annotate(
        dcount=Count('workboard')))
    workboards = all_workboards.filter(pk__in=[d['workboard'] for d in valid_workboards])
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


@csrf_exempt
def update_name(request, id=None):
    dashboard = get_object_or_404(Dashboard, id=id)
    dashboard.name = request.POST.get('board_name', None)
    dashboard.save()

    return redirect('projects:show', id=dashboard.project.pk)


def update(request, id=None):
    pass


def destroy(request, id=None):
    pass
