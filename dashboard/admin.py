# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from dashboard.models import Connection, Query

admin.site.register(Connection)
admin.site.register(Query)
