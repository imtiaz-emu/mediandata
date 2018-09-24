from django import forms
from .models import ConnectedDatabase


class ConnectedDatabaseForm(forms.ModelForm):
	class Meta:
		model = ConnectedDatabase
		fields = [
			'database_name', 'database_type', 'custom_name', 'port', 'host_name', 'db_user_name',
			'password', 'table_names'
		]

class ConnectedDatabaseCSVForm(forms.ModelForm):
	class Meta:
		model = ConnectedDatabase
		fields = [
			'file_name', 'file_location',
		]
