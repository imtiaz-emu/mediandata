from django import template
from projects.models import Project
from django.contrib.auth.models import User
from dashboard.models import Dashboard
import json

register = template.Library()


class SetVarNode(template.Node):
    def __init__(self, var_name, var_value):
        self.var_name = var_name
        self.var_value = var_value

    def render(self, context):
        try:
            value = template.Variable(self.var_value).resolve(context)
        except template.VariableDoesNotExist:
            value = ""
        context[self.var_name] = value

        return u""


@register.tag(name='set')
def set_var(parser, token):
    parts = token.split_contents()
    if len(parts) < 4:
        raise template.TemplateSyntaxError("'set' tag must be of the form: {% set <var_name> = <var_value> %}")

    return SetVarNode(parts[1], parts[3:])


@register.assignment_tag
def user_projects(user_id):
    project_lists = {}
    try:
        user = User.objects.get(id=user_id)
        projects = Project.objects.filter(user=user)
        for proj in projects:
            project_lists[proj.pk] = {
                'name': proj.name,
                'workboards': proj.workboard_set.all(),
                'dashboards': proj.dashboard_set.all()
            }
        return project_lists
    except:
        return project_lists


@register.filter
def get_dict_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def get_json_dict_item(dictionary, key):
    return json.dumps(dictionary.get(key))


@register.assignment_tag
def project_boards(request_path):
    dashboard_id = request_path.split("/dashboards/")[1].replace("/", "")
    project_id = Dashboard.objects.get(id=int(dashboard_id)).project_id
    board_lists = {}
    try:
        project = Project.objects.get(id=project_id)
        board_lists = {
            'name': project.name,
            'workboards': project.workboard_set.all(),
            'dashboards': project.dashboard_set.all()
        }
        return board_lists
    except:
        return board_lists
