from django import forms
from .models import ConnectedDatabase


class ConnectedDatabaseForm(forms.ModelForm):
	class Meta:
		model = ConnectedDatabase
		fields = [
			'database_name', 'database_type', 'custom_name', 'port', 'host_name', 'db_user_name',
			'password', 'table_names'
		]

	def save(self, project = None, conc_string = None):
		db_connection = ConnectedDatabase(
			project = project,
			database_name = self.cleaned_data['database_name'],
			custom_name = self.cleaned_data['custom_name'],
			host_name = self.cleaned_data['host_name'],
			port = self.cleaned_data['port'],
			db_user_name = self.cleaned_data['db_user_name'],
			password = self.cleaned_data['password'],
			connection_string = conc_string,
			database_type = self.cleaned_data['database_type'],
			table_names = self.cleaned_data['table_names'],
			isDatabaseConnection = True,
			save_password = True
		)
		db_connection.save()
		return db_connection


class ConnectedDatabaseCSVForm(forms.ModelForm):
	class Meta:
		model = ConnectedDatabase
		fields = [
			'file_name', 'file_location',
		]

	def save(self, project = None, conc_string = None, table_names = None):
		db_connection = ConnectedDatabase(
			project = project,
			database_name = 'mediandata_uploads',
			custom_name = self.cleaned_data['file_name'],
			host_name = "192.168.3.92",
			port = '5432',
			db_user_name = 'postgres',
			password = 'admin',
			connection_string = conc_string,
			database_type = 'postgresql+psycopg2',
			table_names = table_names,
			isDatabaseConnection = False,
			save_password = True
		)
		db_connection.save()
		return db_connection