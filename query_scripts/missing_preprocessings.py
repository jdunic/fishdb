#!/usr/bin/env python

import csv
import os
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count

from fishdb import settings
from fishdb.models import *
from apps.data.models import *


# Setting django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')

# Creating file
filename = "missing_preprocessings_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

row = ['As of %s, the contained samples do not have preprocessings. Moreso, the fish ones should have them. This has prompted JD to add a treatment "No Treatment" to prevent entry of samples without treatments.']
writer.writerow(row)
writer.writerow('')

no_treat = Samples.objects.select_related().filter(
    preprocessings__fk_Treatment__TreatmentCode=None)
for no in no_treat:
    row = [no.SampleID]
    writer.writerow(row)