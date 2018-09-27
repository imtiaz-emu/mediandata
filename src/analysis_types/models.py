from django.db import models


class AnalysisType(models.Model):
	name = models.CharField(max_length=255)
	title = models.CharField(max_length=255)
	button_class = models.CharField(max_length=255)
	icon_class = models.CharField(max_length=255)
	selected = models.BooleanField(default=False)
	analytics = models.CharField(max_length=500)
	customClass = models.CharField(max_length=255)
