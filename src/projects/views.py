from django.template.loader import render_to_string
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from django.contrib import messages
from .models import Project
from connected_databases.forms import ConnectedDatabaseForm, ConnectedDatabaseCSVForm
from connected_databases.models import ConnectedDatabase
from workboard.models import Workboard
from dashboard.models import Dashboard


@login_required(login_url='/users/signin/')
def index(request):
	projects = Project.objects.filter(user=request.user)
	query = request.GET.get('q')
	if query:
		projects = projects.filter(name__contains=query)
	context = {
		'projects': projects,
		'new_project': ProjectForm(),
		'form_url': '/projects/create/'
	}
	return render(request, "projects/index.html", context)


@login_required(login_url='/users/signin/')
def show(request, id=None):
	project = get_object_or_404(Project, id=id)
	workboards = Workboard.objects.filter(project=project)
	dashboards = Dashboard.objects.filter(project=project)
	try:
		database_connection = ConnectedDatabase.objects.get(project=project)
	except ConnectedDatabase.DoesNotExist:
		database_connection = None

	context = {
		'project': project,
		'edit_project': ProjectForm(instance=project),
		'form_url': '/projects/' + str(id) + '/update/',
		'connection_form': ConnectedDatabaseForm(),
		'upload_form': ConnectedDatabaseCSVForm(),
		'db_connection': database_connection,
		'workboards': workboards,
		'dashboards': dashboards
	}
	return render(request, "projects/show.html", context)


@login_required(login_url='/users/signin/')
def create(request):
	if request.method == 'POST':
		project_form = ProjectForm(request.POST)
		if project_form.is_valid():
			project = Project()
			project.name = project_form.cleaned_data['name']
			project.description = project_form.cleaned_data['description']
			project.is_public = project_form.cleaned_data['is_public']
			project.user = request.user
			project.save()
			messages.success(request, 'Your project was successfully created!')
			return redirect('projects:show', id=project.id)
		else:
			errors = ' '.join([' '.join(x for x in l) for l in list(project_form.errors.values())])
	else:
		project_form = ProjectForm()

	return render(request, 'projects/edit.html', {
		'project_form': project_form,
		'errors': errors
	})



@login_required(login_url='/users/signin/')
def update(request, id=None):
	instance = get_object_or_404(Project, id=id)
	if request.method == 'POST':
		project_form = ProjectForm(request.POST, instance=instance)
		if project_form.is_valid():
			project_form.save()
			messages.success(request, 'Your project was successfully updated!')
			return redirect('projects:show', id=id)
		else:
			errors = ' '.join([' '.join(x for x in l) for l in list(project_form.errors.values())])
	else:
		project_form = ProjectForm(instance=instance)

	return render(request, 'projects/edit.html', {
		'project_form': project_form,
		'errors': errors
	})


@login_required(login_url='/users/signin/')
def destroy(request, id=None):
	project = get_object_or_404(Project, id=id)
	project.delete()
	messages.success(request, 'Your project was successfully deleted!')
	return redirect('projects:index')


@csrf_exempt
def update_board(request, id=None):
	if request.POST.get('type', None) == 'workboard':
		workboard = get_object_or_404(Workboard, id=request.POST.get('board_id', None))
		json_data = {
			'workboard': workboard,
			'board_type': 'workboard',
			'url': '/workboards/' + str(workboard.id) + '/update_name'
		}
	else:
		dashboard = get_object_or_404(Dashboard, id=request.POST.get('board_id', None))
		json_data = {
			'dashboard': dashboard,
			'board_type': 'dashboard',
			'url': '/dashboards/' + str(dashboard.id) + '/update_name'
		}

	template = render_to_string('projects/edit_board_name.html', json_data)
	return HttpResponse(json.dumps(template), content_type='application/json')
