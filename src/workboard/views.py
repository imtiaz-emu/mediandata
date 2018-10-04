from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
import json
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from .models import Workboard
from analysis_types.models import AnalysisType
from connected_databases.models import ConnectedDatabase


# Create your views here.
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
		print(fullVariablesList)
		return json.dumps(fullVariablesList)

	except Exception as e:
		print(e)
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
		return 'fa fa-stripe'
	elif column_type == 'integer':
		return 'fa fa-list-ol'
	else: return 'fa fa-calender'