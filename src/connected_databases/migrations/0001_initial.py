# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-24 05:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConnectedDatabase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('database_name', models.CharField(max_length=255, null=True)),
                ('custom_name', models.CharField(max_length=255, null=True)),
                ('host_name', models.CharField(max_length=255, null=True)),
                ('port', models.IntegerField(null=True)),
                ('db_user_name', models.CharField(max_length=255, null=True)),
                ('password', models.CharField(max_length=255, null=True)),
                ('password_hash', models.CharField(default='Test', max_length=255, null=True)),
                ('connection_string', models.CharField(max_length=255, null=True)),
                ('save_password', models.BooleanField()),
                ('database_type', models.CharField(max_length=255, null=True)),
                ('database_description', models.CharField(max_length=255, null=True)),
                ('advanced', models.CharField(max_length=255, null=True)),
                ('table_names', models.CharField(max_length=10000, null=True)),
                ('isDatabaseConnection', models.BooleanField(default=False)),
                ('file_name', models.CharField(max_length=255, null=True)),
                ('file_location', models.FileField(null=True, upload_to='csv_files/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='projects.Project')),
            ],
        ),
    ]
