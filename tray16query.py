#!/usr/bin/env python
import os
import csv
#import collections
from datetime import datetime

from django.core.management import setup_environ

from fishdb import settings
from apps.data.models import *
from apps.helpers.models import *

setup_environ(settings)

# List of packed samples from KI12TRAY16
# Looking for packed samples, tray position, weight, packed sample PK ID
dt_now = datetime.now().strftime('_%Y_%m_%d')
filename = "KI12TRAY16%s.csv" % dt_now


writer = csv.writer(open(filename, 'wb'), dialect='excel')
row = [
		"PackedSampleID",
		"Position",
		"Weight"
	]
writer.writerow(row)
	
# all_packed = PackedSamples.objects.all()
tray_16 = PackedSamples.objects.filter(fk_TrayName__TrayName='KI12TRAY16')
for ps in tray_16:
	ps_id = ps.id
	ps_pos_join = ps.TrayRow + str(ps.TrayColumn)
	ps_weight = ps.SampleWeight
	psrow = [ps_id, ps_pos_join, ps_weight]
	writer.writerow(psrow)
