from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=255, null=True)
	description = models.CharField(max_length=1000)
	is_public = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

