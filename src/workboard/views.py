from django.shortcuts import render
from .models import Workboard
from django.shortcuts import render, redirect, get_object_or_404


# Create your views here.
def show(request, id=None):
	workboard = get_object_or_404(Workboard, id=id)
	workboards = Workboard.objects.filter(project=workboard.project)
	context = {
		'workboard': workboard,
		'workboards': workboards
	}
	return render(request, "workboards/show.html", context)
