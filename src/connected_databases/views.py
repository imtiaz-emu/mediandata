from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ConnectedDatabaseForm
from django.contrib import messages
from .models import ConnectedDatabase
from projects.models import Project

# Create your views here.
def connect(request, project_id=None):
	pass


def create_db(request, project_id=None):
	pass


def create_csv(request, project_id=None):
	pass
