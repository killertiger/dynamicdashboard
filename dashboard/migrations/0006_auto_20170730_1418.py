# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 14:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_query_visualization_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='DashboardItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Dashboard')),
            ],
        ),
        migrations.AlterField(
            model_name='query',
            name='visualization_type',
            field=models.CharField(choices=[(b'1', b'discreteBarChart'), (b'2', b'multiBarChart'), (b'3', b'pieChart'), (b'0', b'table')], max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='dashboarditem',
            name='query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.Query'),
        ),
    ]
