#!/usr/bin/env python

import csv
import logging
import os
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count

from fishdb import settings
from fishdb.models import *

# Setting django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

logging.basicConfig(level=logging.INFO)

# Creating file
date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')

"""
filename = "pi_todo_list_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

row = ['Counts by functional group of the reliable SI results we have. These are samples that are non-acidified and have either been sent to UVic or UCDavis for analysis.']
"""

# Getting 'reliable' results:
# Those which were sent to UCDavis or UVic for analysis, non-acidified, and fish
results = Results.objects.select_related().filter(Lab__in=['UCDavis', 'UVic'])
na_treat = results.filter(
    fk_Packed__fk_Sample__preprocessings__fk_Treatment__TreatmentCode='NA')

fish_cnt = na_treat.filter(
    fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='fish')

cnt_reliable = fish_cnt.count()
print cnt_reliable


trays = Trays.objects.select_related().filter(Submitted=True).exclude(TrayName__in=['RT_KI_03', 'adrianburrillSFUtray4'])


sublist = [0]
f_list = [0]
m_list = [0]
s_list = [0]

reslist = [0]
res_fish = [0]
res_macr = [0]
res_shar = [0]

for tray in trays:
    ps = tray.packedsamples_set.all()   # gets submitted samples
    cnt_sub = ps.count()
    sublist.append(cnt_sub)   # Total number of submitted samples

    fishes = tray.packedsamples_set.filter(fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='fish')
    cnt_fish = fishes.count()
    f_list.append(cnt_fish)

    macros = tray.packedsamples_set.filter(
        fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='macro')
    cnt_macro = macros.count()
    m_list.append(cnt_macro)

    sharks = tray.packedsamples_set.filter(
        fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='shark') 
    cnt_shark = sharks.count()
    s_list.append(cnt_shark)

    for p in ps:
        res = p.results_set.all() # gets all existing results
        cnt_res = res.count()
        reslist.append(cnt_res)

    for f in fishes:
        res = f.results_set.all()
        cnt_res = res.count()
        res_fish.append(cnt_res)

    for m in macros:
        res = f.results_set.all()
        cnt_res = res.count()
        res_macr.append(cnt_res)

    for s in sharks:
        res = f.results_set.all()
        cnt_res = res.count()
        res_shar.append(cnt_res)




#print sum(sublist)
#print sum(reslist)
#print len(reslist)
waiting_on = sum(sublist) - sum(reslist)
fish_wait = sum(f_list) - sum(res_fish)
macro_wait = sum(m_list) - sum(res_macr)
shark_wait = sum(s_list) - sum(res_shar)

print " > we are waiting on %s from Shapna" % waiting_on
print " > %s fish samples" % fish_wait
print " > %s macro samples" % macro_wait
print " > %s shark samples" % shark_wait































































