#!/usr/bin/env python

# good coding practice restricts line length to 80 characters
# python generally uses '_' to separate words in variable names (not periods!)

# python imports:
import csv
import os
from datetime import datetime

# django imports:
from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist

# importing django settings and the necessary database models:
from fishdb import settings
from apps.data.models import *
from apps.helpers.models import *
from apps.sharks.models import *
from apps.species.models import *

# Setting the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

# Making some dates (gets today's date) and formatting to use in filenames and
# file headers.  See python docs for strftime options
date = datetime.now().strftime('%b%d')  # 
date_y = datetime.now().strftime('%b %d, %Y')

# Setting up the csv file:
filename = "lost_samples_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

writer.writerow(['Record of samples lost from trays KI12TRAY1-14 for which we do not have any results for'])

writer.writerow([''])

row = [
    'SampleID',
    'Species Type',
    'Original Tray'
    ]

ki12_samples = Samples.objects.filter(packedsamples__fk_TrayName__TrayName__in=[
    'KI12TRAY1', 'KI12TRAY2', 'KI12TRAY3', 'KI12TRAY4', 'KI12TRAY5',
    'KI12TRAY6', 'KI12TRAY7', 'KI12TRAY8', 'KI12TRAY9', 'KI12TRAY10',
    'KI12TRAY11', 'KI12TRAY12', 'KI12TRAY13', 'KI12TRAY14'])

results = Results.objects.all()

lost_samples = ki12_samples.exclude(packedsamples__results__in=results) \
    .exclude(packedsamples__fk_TrayName__TrayName__in=
        ['KI12TRAY15', 'KI12TRAYSpares/Duplicates'])

for sample in lost_samples:
    sample_id = sample.SampleID
    stype = sample.fk_Specimen.fk_Species.fk_Type.Type
    trays = sample.packedsamples_set.values_list('fk_TrayName__TrayName', flat=True)
    orig_tray = ', '.join(trays)


    row = [
        sample_id,
        stype,
        orig_tray
        ]

    writer.writerow(row)


















