#!/usr/bin/env python
import csv
import os

from django.core.management import setup_environ
from django.db.models import Q

from fishdb import settings
from fishdb.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

filename = "RT_KI_03_packinglist.csv"

writer = csv.writer(open(filename, 'wb'), dialect='excel')

packed = PackedSamples.objects.select_related().filter(
    fk_TrayName__TrayName = "RT_KI_03")

row = [
    "Tray",
    "Sample",
    "Weight",
    "Spot",
    "OldID"
    ]

writer.writerow(row)

for p in packed:
    sample = str(p.fk_Sample.SampleID)
    row = p.TrayRow
    column = p.TrayColumn
    sample_wt = p.SampleWeight
    notes = p.Notes
    spot = str(row + str(column))
    tray = p.fk_TrayName.TrayName
    oldID = p.fk_Sample.OldSampleID

    row = [
        tray,
        sample,
        sample_wt,
        spot,
        oldID
        ]

    writer.writerow(row)













