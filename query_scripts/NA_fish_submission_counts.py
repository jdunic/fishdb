#!/usr/bin/env python

import csv
import logging
import os
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count, Sum
from django.core.exceptions import ObjectDoesNotExist

from fishdb import settings
from fishdb.models import *


# Selecting all fish samples with treatment: 'NA' and submitted samples from 
# UCDavis and UVic analyses
# What we HAVE:

fish = Samples.objects.filter(fk_Specimen__fk_Species__fk_Type__Type='fish')
na = fish.filter(preprocessings__fk_Treatment__TreatmentCode='NA')
good_trays = na.exclude(packedsamples__fk_TrayName__TrayName='RTKI-001')
submitted = good_trays.filter(packedsamples__fk_TrayName__Submitted=True)

sub_cnt = submitted.values('fk_Specimen__fk_Species__fk_Guild__GuildCode').annotate(submit_cnt=Count('fk_Specimen__fk_Species__fk_Guild__GuildCode'))

fgs = submitted.values_list(
    'fk_Specimen__fk_Species__fk_Guild__GuildCode', flat=True).distinct()

print " > "
print " > The following is the breakdown of submitted NA fish samples"
print " > ---------------"
for i in range(0, fgs.count()):
    fg = sub_cnt[i]['fk_Specimen__fk_Species__fk_Guild__GuildCode']
    count = sub_cnt[i]['submit_cnt']
    print " > %s: %s" % (fg, count)

    row = [
        fg,
        count
    ]

# How many fish have we not yet submitted for analysis and what stage in the
# process are these fish missing:

# 1 - select ALL fish specimens:
# and exclude the CHRMAR CW samples lost from the Stanford freezer
fish = Specimens.objects.select_related().filter(
    fk_Species__fk_Type__Type='fish').exclude(
    CollectionNotes__contains='all samples for Chromis margaritifer were lost from the Stanford freezer')


### A ### - Probs dissections needed:
# 2 - get all of the fish that have no samples

samples = Samples.objects.select_related()
A = fish.exclude(samples__in=samples).distinct() # A = fish without any samples

print ' > Specimens that do not have any samples: %s' % A.count()


### B ### - Will need washing/drying:
# 3 - get all of the fish that have no 'NA' samples but have been dissected

# gets 'NA' samples
na_samples = samples.filter(preprocessings__fk_Treatment__TreatmentCode='NA').distinct()

B = fish.exclude(samples__in=A).exclude(samples__in=na_samples)
print ' > Specimens that do not have "NA" samples: %s' % B.count()


### C ###
# 4 - get fish that do have 'NA' samples but which have not been packed
packed = PackedSamples.objects.select_related()



# Getting specimens that do have 'NA' samples that have not been packed or 
# submitted
na_samps = Samples.objects.select_related().filter(preprocessings__fk_Treatment__TreatmentCode='NA')

a_samps = Samples.objects.select_related().filter(preprocessings__fk_Treatment__TreatmentCode='A')

no_na_samps = no_chrmar.exclude(samples__in=na_samps)

print ' > Specimens that do not have "NA" samples: %s' % no_na_samps.count()

# Getting specimens that HAVE 'NA' samples but have NOT been packed
na_specs = no_chrmar.filter(samples__in=na_samps).distinct()
print ' > %s specimens have existing "NA" samples' % na_specs.count()

packed = PackedSamples.objects.select_related()

not_packed = no_chrmar.exclude(samples__in=)


for f in fish:
    samples = f.samples_set.all()
    spec_no_samp = f.exclude(samples__in=samples)

f.exclude(samples__in=samples)

    if samples is None or samples == '':
        print "Specimen %s has no sample" % fish.SpecimenID
        row = [
            fish.SpecimenID,
            'No Sample Exists'
            ]


    if no_samples:










































