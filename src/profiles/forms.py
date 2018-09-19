from django import forms
from .models import Profile
from django.contrib.auth.models import User


class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ['user', 'updated_at']

		fields = [
			'job_title', 'organization_name', 'phone_country_code', 'phone_number',
			'description', 'url', 'address', 'photo'
		]


class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'first_name',
			'last_name'
		]
