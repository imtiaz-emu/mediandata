from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User

# Create your views here.
def login(request):
  return render(request, "users/login.html", {})

def show(request, id=None):
  pass

def register(request):
  return render(request, "users/register.html", {})

def create(request):
  pass