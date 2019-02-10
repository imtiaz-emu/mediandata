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
    variables = {}
    valid_workboards = []
    all_workboards = Workboard.objects.filter(project=dashboard.project)

    for workboard in all_workboards:
        selectedVariables = SelectedVariables.objects.filter(workboard=workboard)
        variables[workboard.id] = {}
        if len(selectedVariables) > 0:
            variables[workboard.id][selectedVariables[0].table_name] = []
            for variable in selectedVariables:
                variables[workboard.id][variable.table_name].append({
                    'name': variable.column_name,
                    'type': variable.column_type,
                    'id': variable.variable_id
                })
            valid_workboards.append(workboard.id)

    workboards = all_workboards.filter(pk__in=valid_workboards).select_related('analysis_type')
    dashboards = Dashboard.objects.filter(project=dashboard.project)
    context = {
        'dashboard': dashboard,
        'dashboards': dashboards,
        'workboards': workboards,
        'variables': variables
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
