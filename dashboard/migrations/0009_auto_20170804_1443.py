# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 14:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_query_x_axis_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='visualization_type',
            field=models.CharField(choices=[(b'1', b'discreteBarChart'), (b'4', b'lineChart'), (b'2', b'multiBarChart'), (b'3', b'pieChart'), (b'0', b'table')], max_length=1, null=True),
        ),
    ]
