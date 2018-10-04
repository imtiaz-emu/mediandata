from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Workboard
from analysis_types.models import AnalysisType


# Create your views here.
def show(request, id=None):
	workboard = get_object_or_404(Workboard, id=id)
	workboards = Workboard.objects.filter(project=workboard.project)
	analysis_types = AnalysisType.objects.all()
	context = {
		'workboard': workboard,
		'workboards': workboards,
		'analysis_types': analysis_types
	}
	return render(request, "workboards/show.html", context)
