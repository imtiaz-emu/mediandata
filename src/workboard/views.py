from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
import pandas as pd
from .models import Workboard
from analysis_types.models import AnalysisType
from projects.models import Project
from connected_databases.models import ConnectedDatabase


# Create your views here.
def create(request):
	project = Project.objects.get(id=request.POST.get('project_id'))
	workboard = project.workboard_set.create(
		name='New Workboard',
		analysis_type_id=5
	)
	return redirect('workboard:show', id=workboard.pk)


def show(request, id=None):
	workboard = get_object_or_404(Workboard, id=id)
	workboards = Workboard.objects.filter(project=workboard.project)
	analysis_types = AnalysisType.objects.all()

	context = {
		'workboard': workboard,
		'workboards': workboards,
		'analysis_types': analysis_types,
		'js_tree': get_js_tree(workboard.project)
	}
	return render(request, "workboards/show.html", context)


@csrf_exempt
def data_table(request, id=None):
	workboard = get_object_or_404(Workboard, id=id)
	dbCon = ConnectedDatabase.objects.get(project=workboard.project)
	variables = json.loads(request.POST.get('variables', None))
	engine = create_engine(dbCon.connection_string, echo=True)
	cnx = engine.raw_connection()
	collection_name = list(variables.keys())[0]
	column_names = list(variables[list(variables.keys())[0]])
	query_string = 'Select ' + ','.join(column_names) + ' FROM \"' + collection_name + "\""

	try:
		queryData = pd.read_sql(query_string, cnx)

		resultData = queryData.to_dict('records')
		json_data = {
			'data': resultData,
			'analysis_type': 'table',
			'columns': column_names,
			'workboard': workboard
		}

	except Exception as e:
		json_data = {
			'analysis_type': 'table',
			'error': e.args[0],
			'workboard': workboard
		}

	template = render_to_string('workboards/workboard_chart.html', json_data)
	return HttpResponse(json.dumps(template), content_type='application/json')


@csrf_exempt
def data_chart(request, id=None):
	pass


def get_js_tree(project):
	data_connection = ConnectedDatabase.objects.get(project=project)
	fullVariablesList = []

	try:
		engine = create_engine(data_connection.connection_string)
		insp = reflection.Inspector.from_engine(engine)
		for table in list(data_connection.table_names.split(",")):
			fullVariablesList.append({"id": table, "parent": "#", "text": table,
																"data": {"obj": {"collection_name": table}}})
			for column in insp.get_columns(table.strip()):
				column_type = findColumnType(str(column['type']))
				fullVariablesList.append(
					{
						"data": {
							"objId": {
								"Var_Type": column_type,
								"id": column['name'],
							}
						},
						"icon": findIconType(column_type),
						"id": table + "_" + column['name'],
						"parent": table,
						"text": column['name']
					}
				)
		return json.dumps(fullVariablesList)

	except Exception as e:
		return e


def findColumnType(type):
	type = str(type).upper()
	if type.find('CHAR') != -1:
		print(type.find('CHAR'))
		return 'string'
	elif type.find('FLOAT') != -1:
		return 'integer'
	elif type.find('DOUBLE') != -1:
		return 'integer'
	elif type.find('DECIMAL') != -1:
		return 'integer'
	elif type.find('NUMERIC') != -1:
		return 'integer'
	elif type.find('TEXT') != -1:
		return 'string'
	elif type.find('INT') != -1:
		return 'integer'
	elif type.find('BLOB') != -1:
		return 'string'
	elif type.find('DATE') != -1:
		return 'date'
	elif type.find('TIME') != -1:
		return 'date'
	elif type.find('YEAR') != -1:
		return 'date'
	elif type.find('ENUM') != -1:
		return 'enum'
	else:
		return 'string'


def findIconType(column_type):
	if column_type == 'string':
		return 'fa fa-font'
	elif column_type == 'integer':
		return 'fa fa-list-ol'
	else:
		return 'fa fa-calendar'
