#!/usr/bin/env python

# REPL SETUP
import sys
sys.path.append('/Users/jillian/Databases/fishdb')

import csv
import logging
import os
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count

from fishdb import settings
from apps.data.models import *
from apps.species.models import *

# Setting django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

logging.basicConfig(level=logging.INFO)

# Creating file
date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')

"""
filename = "si_results_status_counts_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

row = ["Original query file: si_results_status.py"]
writer.writerow(row)
row = ["Query date: %s, by JD" % date_y]
writer.writerow(row)

row = ['']

row = ['Counts by functional group of the reliable SI results we have. These are samples that are non-acidified and have either been sent to UVic or UCDavis for analysis.']
writer.writerow(row)

"""

# Getting a count for the number of 'reliable' results we have for fish 
# specimens. This means the samples which were sent to UCDavis or UVic for analysis, non-acidified, and fish
results = Results.objects.select_related().filter(Lab__in=['UCDavis', 'UVic'])
na_treat = results.filter(
    fk_Packed__fk_Sample__preprocessings__fk_Treatment__TreatmentCode='NA')

na_fish = na_treat.filter(
    fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='fish')

cnt_reliable = na_fish.count()
print "Number of NA fish results from UCDavis and UVic that we have: %s" % \
cnt_reliable
row = "Number of fish samples that we have reliable (NA, UCDavis, UVIc) results for"

#### TO DO: how many fish do we have results for broken down by functional group,
# by species

row = "Number of fish samples that we have reliable (NA, UCDavis, UVIc) results for, broken down by functional group."
writer.writerow(row)
row = ['FG', 'Count']
writer.writerow(row)

na_fish_count = \
na_fish.values('fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Guild__GuildCode') \
    .annotate(results_count=Count('id'))
na_fish_count

na_fish_count = na_fish \
.order_by('fk_Packed__fk_Sample__fk_Specimen').distinct() \
.values('fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Guild__GuildCode') \
.annotate(results_count=Count('id'))
na_fish_count

for f in na_fish_count:
    fg = f['fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Guild__GuildCode']
    count = f['results_count']
    print "fg: %s: %s" % (fg, count)

    row = [
        fg,
        count
        ]
    writer.writerow(row)

# Get number of 'NA' samples that we have reliable results, broken down by species
na_spp_count = \
na_fish.values('fk_Packed__fk_Sample__fk_Specimen__fk_Species__SpeciesCode') \
    .annotate(results_count=Count('id'))

for s in na_spp_count:
    sp = s['fk_Packed__fk_Sample__fk_Specimen__fk_Species__SpeciesCode']
    count = s['results_count']

    row = [
        sp,
        count
        ]






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
    ps = tray.packedsamples_set.all() # gets submitted sample
    cnt_sub = ps.count()
    sublist.append(cnt_sub)   # Total number of submitted samples

    fishes = tray.packedsamples_set.filter(fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='fish') \
        .annotate(fishes_count=Count('results'))
    cnt_fish = fishes.count()
    f_list.append(cnt_fish)
    fishes.values_list('fishes_count', flat=True)

    macros = tray.packedsamples_set.filter(
        fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='macro') \
        .annotate(macros_count=Count('results'))
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































































