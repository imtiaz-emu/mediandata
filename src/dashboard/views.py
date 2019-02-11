import json
from django.http import HttpResponse
from django.template.loader import render_to_string
from sqlalchemy import create_engine
from django.views.decorators.csrf import csrf_exempt
from .models import Dashboard
from workboard.models import Workboard, SelectedVariables
from projects.models import Project
from django.shortcuts import render, redirect, get_object_or_404
from connected_databases.models import ConnectedDatabase
import pandas as pd

# Create your views here.
def show(request, id=None):
    dashboard = get_object_or_404(Dashboard, id=id)
    variables = {}
    valid_workboards = []
    all_workboards = Workboard.objects.filter(project=dashboard.project)

    for workboard in all_workboards:
        selectedVariables = SelectedVariables.objects.filter(workboard=workboard)
        variables[workboard.id] = {}
        if len(selectedVariables) > 0:
            variables[workboard.id][selectedVariables[0].table_name] = []
            for variable in selectedVariables:
                variables[workboard.id][variable.table_name].append({
                    "name": variable.column_name,
                    "type": variable.column_type,
                    "id": variable.variable_id
                })
            valid_workboards.append(workboard.id)

    workboards = all_workboards.filter(pk__in=valid_workboards).select_related('analysis_type')
    dashboards = Dashboard.objects.filter(project=dashboard.project)
    context = {
        'dashboard': dashboard,
        'dashboards': dashboards,
        'workboards': workboards,
        "variables": variables
    }
    return render(request, "dashboards/show.html", context)


def create(request):
    project = Project.objects.get(id=request.POST.get('project_id'))
    dashboard = project.dashboard_set.create(
        name='New Dashboard'
    )
    return redirect('dashboard:show', id=dashboard.pk)


@csrf_exempt
def update_name(request, id=None):
    dashboard = get_object_or_404(Dashboard, id=id)
    dashboard.name = request.POST.get('board_name', None)
    dashboard.save()

    return redirect('projects:show', id=dashboard.project.pk)


def update(request, id=None):
    pass


def destroy(request, id=None):
    pass


@csrf_exempt
def data_table(request, id=None):
	workboard = get_object_or_404(Workboard, id=id)
	dbCon = ConnectedDatabase.objects.get(project=workboard.project)
	variables = json.loads(request.POST.get('variables', None))
	engine = create_engine(dbCon.connection_string, echo=True)
	cnx = engine.raw_connection()
	collection_name = list(variables.keys())[0]
	column_names = [x['name'] for x in variables[collection_name]]
	# column_types = [x['type'] for x in variables[collection_name]]
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
	dashboard = get_object_or_404(Dashboard, id=id)
	dbCon = ConnectedDatabase.objects.get(project=dashboard.project)
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
			'workboard': dashboard
		}

	except Exception as e:
		json_data = {
			'analysis_type': request.POST.get('type', None),
			'error': e.args[0],
			'workboard': dashboard
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
