from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .forms import ProfileForm, UserForm
from django.contrib import messages
from .models import Profile


def show(request, id=None):
	instance = get_object_or_404(Profile, id=id)
	return render(request, "profiles/show.html", {'profile': instance})


def edit(request, id=None):
	instance = get_object_or_404(Profile, id=id)
	user_form = UserForm(instance=instance.user)
	profile_form = ProfileForm(instance=instance)
	errors = ''
	return render(request, 'profiles/edit.html', {
		'user_form': user_form,
		'profile_form': profile_form,
		'errors': errors
	})


def update(request, id=None):
	instance = get_object_or_404(Profile, id=id)
	if request.method == 'POST':
		user_form = UserForm(request.POST, instance=instance.user)
		profile_form = ProfileForm(request.POST, instance=instance)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, 'Your profile was successfully updated!')
			return redirect('profiles:show')
		else:
			errors = ' '.join([' '.join(x for x in l) for l in list(profile_form.errors.values())])
	else:
		user_form = UserForm(instance=instance.user)
		profile_form = ProfileForm(instance=instance)

	return render(request, 'profiles/edit.html', {
		'user_form': user_form,
		'profile_form': profile_form,
		'errors': errors
	})