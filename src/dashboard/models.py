from django.db import models
from projects.models import Project
from workboard.models import Workboard


class Dashboard(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	order_rank = models.IntegerField(null=True, blank=True)
	show = models.BooleanField(default=True)
	locked = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
	workboards = models.ManyToManyField(Workboard)
