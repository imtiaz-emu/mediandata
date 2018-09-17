from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login


def login(request):
	errors = None
	f = CustomUserLoginForm()
	if request.method == 'POST':
		f = CustomUserLoginForm(request.POST)
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, email=email, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'Signed in Successfully!')
			return redirect('profiles:show')
		else:
			errors = 'Invalid Login credentials!'

	return render(request, "users/login.html", {'errors': errors, 'form': f})

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
