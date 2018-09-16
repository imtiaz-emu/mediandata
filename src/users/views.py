from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.contrib import messages


def login(request):
  return render(request, "users/login.html", {})

def show(request, id=None):
  pass

def register(request):
  if request.method == 'POST':
    f = CustomUserCreationForm(request.POST)
    if f.is_valid():
      f.save()
      messages.success(request, 'Account created successfully')
      return redirect('users:register')

  else:
    f = CustomUserCreationForm()

  errors = ' '.join([' '.join(x for x in l) for l in list(f.errors.values())])

  return render(request, "users/register.html", {'form': f, 'errors': errors})

def create(request):
  pass