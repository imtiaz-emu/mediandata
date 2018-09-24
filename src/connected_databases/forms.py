from django import forms
from .models import ConnectedDatabase


class ConnectedDatabaseForm(forms.ModelForm):
   class Meta:
       model = ConnectedDatabase
       fields = ['database_name', 'database_type']
