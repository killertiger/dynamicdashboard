# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
#class BaseModel(models.Model):
#    last_update = models.DateTimeField(auto_now=True)
#    create_date = models.DateTimeField(auto_now_add=True)
from dashboard.utils import ChoiceEnum


class Connection(models.Model):
    name = models.CharField(max_length=200)
    host = models.GenericIPAddressField(protocol='IPv4', null=True)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    defaultDatabase = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class VisualizationTypes(ChoiceEnum):
    table = 0
    discreteBarChart = 1
    multiBarChart = 2
    pieChart = 3


class Query(models.Model):
    name = models.CharField(max_length=200)
    text = models.TextField()
    description = models.TextField(null=True, blank=True)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, null=True)
    visualization_type = models.CharField(max_length=1, choices=VisualizationTypes.choices(), null=True)
    x_axis_field = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name


class Dashboard(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    @property
    def dashboarditems(self):
        return DashboardItem.objects.filter(dashboard=self.pk)

    def __str__(self):
        return self.name


class DashboardItem(models.Model):
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)
    query = models.ForeignKey(Query, on_delete=models.CASCADE)

    def __str__(self):
        return self.dashboard.name + ' - ' + self.query.name

