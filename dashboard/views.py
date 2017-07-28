# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def execute_query(question_id):
    
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                         user="john",         # your username
                         passwd="megajonhy",  # your password
                         db="jonhydb")        # name of the data base


    return render(request, )