#!/usr/bin/python

#learning, nothing new here.

from django.core.management import setup_environ
import settings
setup_environ(settings)
from django.db import models
from apps.images.models import *
import time

import csv

filename = "specimen_export%s.csv" % time.time()

writer = csv.writer(open(filename, 'wb'), dialect='excel')

specimens = Specimens.objects.all()
species = Species.objects.all()
sites = Sites.objects.all()
row = [
    "SpecimenID",
    "SpeciesCode",
    "Site"
    ]

writer.writerow(row)

for specimen in specimens:
    sp = Specimens.objects.filter(fk_Species__id=SpeciesCode)
    site = Specimens.objects.filter(fk_Site__id=SiteName)

    row = [
        Specimens.objects.SpecimenID,
        sp,
        site
        ]
    writer.writerow(row)
