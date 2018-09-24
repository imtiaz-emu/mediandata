from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from django.contrib import messages
from .models import Project


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
	context = {
		'project': project,
		'edit_project': ProjectForm(instance=project),
		'form_url': '/projects/' + str(id) + '/update/'
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

