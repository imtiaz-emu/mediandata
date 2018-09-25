from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json
import urllib
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
import pandas as pd
from .forms import ConnectedDatabaseForm
from django.contrib import messages
from .models import ConnectedDatabase
from projects.models import Project

# Create your views here.
def connect(request, project_id=None):
	project = Project.objects.get(id=project_id)
	connection_string = database_string_creation(request.POST)
	if request.POST.get("submit") == 'connect':
		json_data = {
			'tables': [],
			'errors': []
		}
		try:
			engine = create_engine(connection_string)
			insp = reflection.Inspector.from_engine(engine)

			for i, table in enumerate(insp.get_table_names()):
				json_data['tables'].append({'id': i, 'name': table, 'checked': False})
			if not json_data['tables']:
				json_data['errors'].append("Please create some tables in your database")
		except Exception as e:
			if hasattr(e, 'orig'):
				if hasattr(e.orig, 'message'):
					if (e.orig.message):
						json_data['errors'].append(e.orig.message)
					else:
						json_data['errors'].append("Error Code: " + str(e.orig[0]) + " Error Message: " + e.orig[1])
				elif hasattr(e.orig, 'args'):
					json_data['errors'].append(e.orig.args[len(e.orig.args) - 1])
			else:
				json_data['errors'].append("Sorry can not connect to database, check your connection information")

	return HttpResponse(json.dumps({'data': json_data}), content_type='application/json')


def create_db(request, project_id=None):
	pass


def create_csv(request, project_id=None):
	pass


def database_string_creation(post_data):
	if (post_data['database_type'] == 'mssql'):
		database_string = "DRIVER={SQL Server};SERVER=" + post_data['host_name'] + "\MSSQL2008R2;PORT=" + \
											post_data['port'] + \
											";DATABASE=" + post_data['database_name'] + ";UID=" + post_data[
												'db_user_name'] + ";PWD=" + post_data['password'] + ";"
		database_string = urllib.parse.quote(database_string)
		database_string = "mssql+pyodbc:///?odbc_connect=%s" % database_string

	else:
		database_string = str(post_data.get("database_type")) + "://" + str(
		post_data.get("db_user_name")) + ":" + str(
		post_data.get("password")) + "@" + str(post_data.get("host_name")) + ":" + str(
		post_data.get("port")) + "/" + str(post_data.get("database_name"))

	return database_string