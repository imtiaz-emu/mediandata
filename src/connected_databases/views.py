from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json
import urllib
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from django.template.loader import render_to_string
import pandas as pd
from .forms import ConnectedDatabaseForm, ConnectedDatabaseCSVForm
from django.contrib import messages
from .models import ConnectedDatabase
from projects.models import Project
from workboard.models import Workboard
from dashboard.models import Dashboard


# Create your views here.
def connect(request, project_id=None):
	project = Project.objects.get(id=project_id)
	connection_string = database_string_creation(request.POST)
	if request.POST.get("submit") == 'connect':
		json_data = {
			'tables': [],
			'errors': ''
		}
		try:
			engine = create_engine(connection_string)
			insp = reflection.Inspector.from_engine(engine)

			for i, table in enumerate(insp.get_table_names()):
				json_data['tables'].append({'id': i, 'name': table, 'checked': False})
			if not json_data['tables']:
				json_data['errors'] = "Please create some tables in your database"
		except Exception as e:
			if hasattr(e, 'orig'):
				if hasattr(e.orig, 'message'):
					if (e.orig.message):
						json_data['errors'] = e.orig.message
					else:
						json_data['errors'] = ("Error Code: " + str(e.orig[0]) + " Error Message: " + e.orig[1])
				elif hasattr(e.orig, 'args'):
					json_data['errors'] = (e.orig.args[len(e.orig.args) - 1])
			else:
				json_data['errors'] = "Sorry can not connect to database, check your connection information"

		template = render_to_string('projects/connection_info.html', json_data)
		return HttpResponse(json.dumps(template), content_type='application/json')
	elif request.POST.get("table_names"):
		db_form = ConnectedDatabaseForm(request.POST)
		if db_form.is_valid():
			db_form.save(project, database_string_creation(request.POST))
			default_work_dash_board_create(project)
			messages.success(request, 'Database Connection was successfully Saved!')
			return redirect('projects:show', id=project.id)
		else:
			errors = ' '.join([' '.join(x for x in l) for l in list(db_form.errors.values())])
			return HttpResponse(json.dumps(errors), content_type='application/json')


def create_csv(request, project_id=None):
	project = Project.objects.get(id=project_id)
	csv_form = ConnectedDatabaseCSVForm(request.POST, request.FILES or None)
	if csv_form.is_valid():
		try:
			con_string = 'postgresql://postgres:admin@localhost:5432/mediandata_uploads'
			engine = create_engine(con_string)
			customTablenames = []

			if request.FILES['file_location'].name.endswith('.csv'):
				data = pd.read_csv(request.FILES['file_location'])
				tempName = project.name + "_" + project_id
				customTablenames.append(tempName.replace(" ", "_"))
				data.to_sql(customTablenames[-1], engine)
			else:
				data_sheets = pd.ExcelFile(request.FILES['file_location'])
				for sheet in data_sheets.sheet_names:
					data = pd.read_excel(data_sheets, data_sheets.sheet_names[0])
					tempName = project.name + "_" + project_id + "_" + sheet
					customTablenames.append(tempName.replace(" ", "_"))
					data.to_sql(customTablenames[-1], engine)

			csv_form.save(project, con_string, ",".join(customTablenames))
			default_work_dash_board_create(project)
			messages.success(request, 'Database Connection was successfully Saved!')
			return redirect('projects:show', id=project.id)
		except Exception as e:
			return HttpResponse(json.dumps(str(e)), content_type='application/json')

	return HttpResponse(json.dumps(csv_form.errors.values()), content_type='application/json')


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


def default_work_dash_board_create(project):
	project.dashboard_set.create(
		name='New Dashboard'
	)
	project.workboard_set.create(
		name='New Workboard',
		analysis_type_id=5
	)


