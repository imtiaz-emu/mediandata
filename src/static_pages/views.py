from django.shortcuts import render, redirect
from .decorators import anonymous_required


@anonymous_required
def home(request):
	return render(request, "static_pages/home.html")