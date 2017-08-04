# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pymysql
from django.shortcuts import render
from nvd3 import discreteBarChart, multiBarChart, pieChart, lineChart
import datetime, time

from dashboard.models import Query, Connection, Dashboard


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


def createchart(visualization_type, rows, xaxisfield):
    chart = None
    if not rows:
        return None

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
        # chart = multiBarHorizontalChart(width=500, height=400, x_axis_format=None)

        xdata = []
        ydata = []


        for row in rows:
            xdata.append(row[xaxisfield])

        for key in rows[0]:
            if key == xaxisfield:
                continue
            for row in rows:
                ydata.append(row[key])

            chart.add_serie(name=key, y=ydata, x=xdata)
            ydata = []

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

    elif visualization_type == '4':
        chart = lineChart(name='lineChart', height=400, width=1300, x_is_date=True)

        xdata = []
        ydata = []

        for row in rows:
            xdata.append(row[xaxisfield])

        for key in rows[0]:
            if key == xaxisfield:
                continue
            for row in rows:
                ydata.append(row[key])


        xdata = [datetime.datetime.strptime(s, "%m/%Y") for s in xdata]
        xdata = [time.mktime(s.timetuple()) * 1000 for s in xdata]

        chart.add_serie(name="line", y=ydata, x=xdata)

    if chart:
        chart.buildcontent()

    return chart


def formatquery(variables, querytext):
    for key in variables:
        querytext = querytext.replace('{{' + key + '}}', variables[key])

    return querytext


def get_database_name(list, defaultDatabase):
    if 'database' in list:
        return list['database']
    else:
        return defaultDatabase


# Create your views here.
def queryview(request, query_id):
    query = Query.objects.get(pk=query_id)
    connection = query.connection

    querytext = formatquery(request.GET, query.text)
    database = get_database_name(request.GET, connection.defaultDatabase)
    rows = execute_query(connection, database, querytext)

    chart = createchart(query.visualization_type, rows, query.x_axis_field)

    return render(request, context={'rows': rows, 'chart': chart}, template_name='dashboard/query.html')


def dashboardview(request, dashboard_id):
    dashboard = Dashboard.objects.get(pk=dashboard_id)

    connection = Connection.objects.get(pk=1)
    database = get_database_name(request.GET, connection.defaultDatabase)

    charts = []

    for dashboarditem in dashboard.dashboarditems:
        querytext = formatquery(request.GET, dashboarditem.query.text)
        rows = execute_query(connection, database, querytext)
        chart = createchart(dashboarditem.query.visualization_type, rows, dashboarditem.query.x_axis_field)
        charts.append(chart)

    context = {'charts':  charts}

    return render(request, context=context, template_name='dashboard/index.html')
