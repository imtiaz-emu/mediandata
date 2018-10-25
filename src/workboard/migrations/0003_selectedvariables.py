# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-25 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workboard', '0002_remove_workboard_default_zoom'),
    ]

    operations = [
        migrations.CreateModel(
            name='SelectedVariables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('column_name', models.CharField(max_length=255)),
                ('column_type', models.CharField(max_length=255)),
                ('table_name', models.CharField(max_length=255)),
                ('aggregation_value', models.CharField(blank=True, max_length=255, null=True)),
                ('workboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workboard.Workboard')),
            ],
        ),
    ]
