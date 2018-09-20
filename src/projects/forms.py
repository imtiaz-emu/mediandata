from django import forms
from .models import Project


class ProjectForm(forms.Form):
	name = forms.CharField(max_length=255, required=True)
	description = forms.CharField(widget=forms.Textarea, required=True)
	is_public = forms.BooleanField(required=False)
