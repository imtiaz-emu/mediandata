from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from static_pages.decorators import anonymous_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


@anonymous_required
def signin(request):
	errors = None
	f = CustomUserLoginForm()
	if request.method == 'POST':
		f = CustomUserLoginForm(request.POST)
		email = request.POST['email']
		password = request.POST['password']
		try:
			user = User.objects.get(email=email)
			username = user.username
		except User.DoesNotExist:
			username = None
		auth_user = authenticate(request, username=username, password=password)
		if auth_user is not None:
			login(request, auth_user)
			messages.success(request, 'Signed in Successfully!')
			return redirect('profiles:show', id=user.profile.id)
		else:
			errors = 'Invalid Login credentials!'

	return render(request, "users/login.html", {'errors': errors, 'form': f})


@anonymous_required
def register(request):
	if request.method == 'POST':
		f = CustomUserCreationForm(request.POST)
		if f.is_valid():
			f.save()
			messages.success(request, 'Account created successfully')
			return redirect('users:signin')

	else:
		f = CustomUserCreationForm()

	errors = ' '.join([' '.join(x for x in l) for l in list(f.errors.values())])

	return render(request, "users/register.html", {'form': f, 'errors': errors})


@login_required(login_url='/users/signin/')
def signout(request):
	logout(request)
	return redirect('users:signin')