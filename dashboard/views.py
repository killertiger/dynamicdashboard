# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymysql
from django.shortcuts import render
from nvd3 import discreteBarChart, multiBarChart, pieChart

from dashboard.models import Query, Connection, VisualizationTypes, Dashboard


def execute_query(connectiondata, database, query):
    connection = pymysql.connect(host=connectiondata.host,
                                 user=connectiondata.username,
                                 password=connectiondata.password,
                                 db=database,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor() as cursor:
        cursor.execute(query=query)
        rows = cursor.fetchall()

    return rows


def createchart(visualization_type, rows):
    chart = None

    if visualization_type == '1':
        xdata = []
        ydata = []

        for key in rows[0]:
            xdata.append(key)
            for row in rows:
                ydata.append(int(row[key]))

        chart = discreteBarChart(name='discreteBarChart', height=400, width=400)

        chart.add_serie(y=ydata, x=xdata)

    elif visualization_type == '2':
        chart = multiBarChart(width=500, height=400, x_axis_format=None)

        xdata = []
        ydata = []

        isfirst = True
        for key in rows[0]:
            for row in rows:
                if isfirst:
                    xdata.append(row[key])
                else:
                    ydata.append(row[key])

            if not isfirst:
                chart.add_serie(name=key, y=ydata, x=xdata)
                ydata = []

            isfirst = False

    elif visualization_type == '3':
        chart = pieChart(name='pieChart', height=400, width=400)

        xdata = []
        ydata = []

        isfirst = True
        for key in rows[0]:
            for row in rows:
                if isfirst:
                    xdata.append(row[key])
                else:
                    ydata.append(row[key])

            if not isfirst:
                chart.add_serie(name=key, y=ydata, x=xdata)
                ydata = []

            isfirst = False

    if chart:
        chart.buildcontent()

    return chart

# Create your views here.
def queryview(request, query_id):
    query = Query.objects.get(pk=query_id)
    connection = Connection.objects.get(pk=1)

    rows = execute_query(connection, connection.defaultDatabase, query.text)

    chart = createchart(query.visualization_type, rows)

    return render(request, context={'rows': rows, 'chart': chart}, template_name='dashboard/query.html')


def dashboardview(request, dashboard_id):
    dashboard = Dashboard.objects.get(pk=dashboard_id)

    connection = Connection.objects.get(pk=1)

    charts = []

    for dashboarditem in dashboard.dashboarditems:
        rows = execute_query(connection, connection.defaultDatabase, dashboarditem.query.text)
        chart = createchart(dashboarditem.query.visualization_type, rows)
        charts.append(chart)

    context = {'charts':  charts}

    return render(request, context=context, template_name='dashboard/index.html')
