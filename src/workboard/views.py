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
	column_names = [x['name'] for x in variables[collection_name]]
	column_types = [x['type'] for x in variables[collection_name]]
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
	workboard = get_object_or_404(Workboard, id=id)
	dbCon = ConnectedDatabase.objects.get(project=workboard.project)
	variables = json.loads(request.POST.get('variables', None))
	engine = create_engine(dbCon.connection_string, echo=True)
	cnx = engine.raw_connection()
	collection_name = list(variables.keys())[0]

	yaxis = []
	column_names = []
	column_types = []
	for item in variables[collection_name]:
		column_names.append(item['name'])
		column_types.append(item['type'])
		if item['type'] == 'string':
			xaxis = item['name']
		else:
			yaxis.append(item['name'])

	finalResult = []

	try:
		for chart_yaxis in yaxis:
			data = pd.read_sql(
				'Select \"' + collection_name + "\".\"" + xaxis + '\" as label, \"' + collection_name + "\".\"" + chart_yaxis + '\" as value FROM \"' + collection_name + "\"",
				cnx)

			datasum = data.groupby(['label']).sum()
			datasum['index_col'] = range(0, len(datasum))
			datamin = data.groupby(['label']).min()
			datamin['index_col'] = range(0, len(datamin))
			datamax = data.groupby(['label']).max()
			datamax['index_col'] = range(0, len(datamax))
			dataavg = data.groupby(['label']).mean()
			dataavg['index_col'] = range(0, len(dataavg))

			resultsumdump = json.JSONDecoder().decode(datasum.reset_index().to_json(orient="records"))
			resultmindump = json.JSONDecoder().decode(datamin.reset_index().to_json(orient="records"))
			resultmaxdump = json.JSONDecoder().decode(datamax.reset_index().to_json(orient="records"))
			resultavgdump = json.JSONDecoder().decode(dataavg.reset_index().to_json(orient="records"))

			finalResult.append(
				{'sum': resultsumdump, 'avg': resultavgdump, 'min': resultmindump, 'max': resultmaxdump,
				 'var_name': chart_yaxis})

		json_data = {
			'data': json.dumps(finalResult),
			'analysis_type': request.POST.get('type', None),
			'columns': column_names,
			'workboard': workboard
		}

	except Exception as e:
		json_data = {
			'analysis_type': request.POST.get('type', None),
			'error': e.args[0],
			'workboard': workboard
		}

	template = render_to_string('workboards/workboard_chart.html', json_data)
	return HttpResponse(json.dumps(template), content_type='application/json')


@csrf_exempt
def data_bubble(request, id=None):
	workboard = get_object_or_404(Workboard, id=id)
	dbCon = ConnectedDatabase.objects.get(project=workboard.project)
	variables = json.loads(request.POST.get('variables', None))
	engine = create_engine(dbCon.connection_string, echo=True)
	cnx = engine.raw_connection()
	collection_name = list(variables.keys())[0]

	column_names = []
	yaxis = None
	for item in variables[collection_name]:
		column_names.append(item['name'])
		if item['type'] == 'string':
			xaxis = item['name']
		elif yaxis == None and item['type'] == 'integer':
			yaxis = item['name']
		elif item['type'] == 'integer':
			zaxis = item['name']

	finalResult = []

	try:
		data = pd.read_sql(
			'Select \"' + collection_name + "\".\"" + xaxis + '\" as x, \"' + collection_name + "\".\"" + yaxis \
			+ '\" as y, \"' + collection_name + "\".\"" + zaxis + '\" as size FROM \"' + collection_name + "\"",
			cnx)

		datasum = data.groupby(['x']).sum()
		datasum['index_col'] = range(0, len(datasum))
		datamin = data.groupby(['x']).min()
		datamin['index_col'] = range(0, len(datamin))
		datamax = data.groupby(['x']).max()
		datamax['index_col'] = range(0, len(datamax))
		dataavg = data.groupby(['x']).mean()
		dataavg['index_col'] = range(0, len(dataavg))

		resultsumdump = json.JSONDecoder().decode(datasum.reset_index().to_json(orient="records"))
		resultmindump = json.JSONDecoder().decode(datamin.reset_index().to_json(orient="records"))
		resultmaxdump = json.JSONDecoder().decode(datamax.reset_index().to_json(orient="records"))
		resultavgdump = json.JSONDecoder().decode(dataavg.reset_index().to_json(orient="records"))

		finalResult.append(
			{'sum': resultsumdump, 'avg': resultavgdump, 'min': resultmindump, 'max': resultmaxdump, 'var_name': xaxis})

		json_data = {
			'data': json.dumps(finalResult),
			'analysis_type': request.POST.get('type', None),
			'columns': column_names,
			'workboard': workboard,
			'yaxis': yaxis,
			'zaxis': zaxis
		}

	except Exception as e:
		json_data = {
			'analysis_type': request.POST.get('type', None),
			'error': e.args[0],
			'workboard': workboard
		}

	template = render_to_string('workboards/workboard_chart.html', json_data)
	return HttpResponse(json.dumps(template), content_type='application/json')


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
						"text": column['name'],
						"var_type": column_type
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
