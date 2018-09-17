from django.contrib.auth.models import User, Group
from django import forms
from django.core.exceptions import ValidationError
import django.contrib.auth.password_validation as validators


class CustomUserCreationForm(forms.Form):
	CHOICES = [('company', 'Company Account'),
						 ('individual', 'Individual Account')]

	role = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect(), required=True)
	username = forms.CharField(label='Enter Username', min_length=5, max_length=150)
	email = forms.EmailField(label='Enter email')
	password = forms.CharField(label='Enter password', widget=forms.PasswordInput)

	def clean_username(self):
		username = self.cleaned_data['username'].lower()
		r = User.objects.filter(username=username)
		if r.count():
			raise ValidationError("Username already exists")
		return username

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		r = User.objects.filter(email=email)
		if r.count():
			raise ValidationError("Email already exists")
		return email

	def clean_password(self):
		password = self.cleaned_data.get('password')
		try:
			validators.validate_password(password=password)

		except ValidationError as e:
			raise ValidationError(e)

		return password

	def save(self, commit=True):
		user = User.objects.create_user(
			self.cleaned_data['username'],
			self.cleaned_data['email'],
			self.cleaned_data['password']
		)
		my_group, _ = Group.objects.get_or_create(name=self.cleaned_data.get('role'))
		my_group.user_set.add(user)

		return user

class CustomUserLoginForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'email', 'password'
		]