from django.db import models
from projects.models import Project


# Create your models here.
class ConnectedDatabase(models.Model):
	DATABASES = (
		("postgresql+psycopg2", "PostgreSQL"),
		("mysql+pymysql", "MySQL"),
		("mssql", "MSSQL")
	)

	project = models.OneToOneField(Project, on_delete=models.CASCADE)
	database_name = models.CharField(max_length=255, null=True)
	custom_name = models.CharField(max_length=255, null=True)
	host_name = models.CharField(max_length=255, null=True)
	port = models.IntegerField(null=True)
	db_user_name = models.CharField(max_length=255, null=True)
	password = models.CharField(max_length=255, null=True)
	password_hash = models.CharField(max_length=255, null=True, default="Test")
	connection_string = models.CharField(max_length=255, null=True)
	save_password = models.BooleanField()
	database_type = models.CharField(max_length=255, null=True, choices=DATABASES, default='postgresql+psycopg2')
	database_description = models.CharField(max_length=255, null=True)
	advanced = models.CharField(max_length=255, null=True)
	table_names = models.CharField(max_length=10000, null=True)

	isDatabaseConnection = models.BooleanField(default=False)
	file_name = models.CharField(max_length=255, null=True)
	file_location = models.FileField(upload_to='csv_files/', null=True)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""Return the model as a string."""

		return self.database_name + ": " + self.custom_name
