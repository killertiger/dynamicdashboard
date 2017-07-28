# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    last_update = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)


class Connection(BaseModel):
    name = models.CharField(max_length=200)
    host = models.GenericIPAddressField()
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    defaultDatabase = models.CharField(max_length=200)


class Query(BaseModel):
    name = models.CharField(max_length=200)
    text = models.CharField(max_length=1000)
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE)
