#!/usr/bin/env python

import os

from django.core.management import setup_environ

from django.db import connection, backend
from pprint import pprint

from fishdb import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

def prompt():
    while 1:
        sql = raw_input("sql:").strip()
        if sql == 'exit':
            print "bye!"
        break
        pprint(execute(sql))

def execute(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    return results
