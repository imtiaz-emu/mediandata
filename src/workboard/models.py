from django.db import models
from projects.models import Project
from analysis_types.models import AnalysisType


class Workboard(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	analysis_type = models.ForeignKey(AnalysisType, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=255)
	filterQuery = models.CharField(max_length=255, null=True, blank=True)
	filterIsValid = models.BooleanField(default=True)
	filter = models.CharField(max_length=400, null=True, blank=True)
	isFavourite = models.BooleanField(default=False)
	chart_title = models.CharField(max_length=100, null=True, blank=True)
	filter_rules = models.TextField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)


class SelectedVariables(models.Model):
	workboard = models.ForeignKey(Workboard, on_delete=models.CASCADE)
	column_name = models.CharField(max_length=255)
	column_type = models.CharField(max_length=255)
	table_name = models.CharField(max_length=255)
	aggregation_value = models.CharField(max_length=255, blank=True, null=True)
	variable_id = models.CharField(max_length=255, default=None)
