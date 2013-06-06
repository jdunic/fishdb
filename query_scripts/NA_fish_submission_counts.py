#!/usr/bin/env python

import csv
import logging
import os
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count, Sum
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from fishdb import settings
from apps.data.models import *
from apps.species.models import *

logging.basicConfig(level=logging.INFO)

# Selecting all fish samples with treatment: 'NA' and submitted samples from 
# UCDavis and UVic analyses
# What we HAVE:
"""
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
for fg in fgs:
    func_group = fg['fk_Specimen__fk_Species__fk_Guild__GuildCode']
    count = fg['submit_cnt']
    print " > %s: %s" % (fg, count)

    row = [
        func_group,
        count
    ]
"""
# Creating file
date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')


filename = "funnel_analysis_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

writer.writerow(['List of specimens that do not have results because they have not progressed through the entire processing chain.'])

# How many fish have we not yet submitted for analysis and what stage in the
# process are these fish missing:

# 1 - select ALL fish specimens:
# and exclude the CHRMAR CW samples that were lost from the Stanford freezer
fish = Specimens.objects.select_related().filter(
    fk_Species__fk_Type__Type='fish').exclude(
    CollectionNotes__contains='all samples for Chromis margaritifer were lost from the Stanford freezer')


### A ### - Probs dissections needed:
# 2 - get all of the fish that have no samples
# Done by getting all fish specimens that are not found in all samples.
samples = Samples.objects.select_related()
dis = Dissections.objects.select_related()

A = fish.exclude(dissections__in=dis)

A = fish.exclude(samples__in=samples).distinct() # A = fish without any samples

print ' > Specimens that do not have any samples: %s' % A.count()

A_list = A.values('fk_Species__fk_Guild__GuildCode',
                  'fk_Species__ScientificName',
                  'fk_Site__SiteName'
                  )

row = [
    'SpecimenID',
    'SpeciesCode',
    'ScientificName',
    'Fg',
    'CollectionNotes',
    'DissectionID',
    'DissectionNotes'
    ]

writer.writerow('')
writer.writerow(['Fish that do not have any samples. Either they have not been dissected or their samples have been lost?'])
writer.writerow(row)

for a in A:
    try:
        specimen = a.SpecimenID
        species = a.fk_Species.SpeciesCode
        sci_name = a.fk_Species.ScientificName
        fg = a.fk_Species.fk_Guild.GuildCode
        spec_notes = a.CollectionNotes
        notes = a.dissections_set.get().Notes
        dis_id = a.dissections_set.get().id
        #print "specimen %s, %s. dis_id: %s, %s" % (specimen, fg, dis_id, notes)
    except AttributeError, e:
        logging.warn('specimen %s %s' % (specimen, e))
    row = [
        specimen,
        species,
        sci_name,
        fg,
        spec_notes,
        dis_id,
        notes]
    writer.writerow(row)


### B ### - Will need washing/drying:
# 3 - get all of the fish that have no 'NA' samples but have been dissected

# gets 'NA' samples
na_samples = samples.select_related() \
    .filter(preprocessings__fk_Treatment__TreatmentCode='NA').distinct()

B = fish.exclude(samples__in=A).exclude(samples__in=na_samples)
print ' > Specimens that do not have "NA" samples: %s' % B.count()

row = [
    'SpecimenID',
    'SpeciesCode',
    'ScientificName',
    'Fg',
    #'SizeClass',
    'Weight',
    'CollectionNotes',
    'DissectionNotes',
    'SampleNotes'
    ]

writer.writerow('')
writer.writerow(['Fish that do not have any NA samples'])
writer.writerow(row)

for b in B:
    specimen = b.SpecimenID
    species = b.fk_Species.SpeciesCode
    sci_name = b.fk_Species.ScientificName
    try:
        fg = b.fk_Species.fk_Guild.GuildCode
    except AttributeError as e:
        logging.warn("%s %s" % (specimen, e))
        print "no functional group assigned to %s" % specimen
        fg = "no functional group assigned to species %s" % species
    size = b.dissections_set.get().SizeClass()
        #try:
    weight = b.dissections_set.get().wt
        #except NameError as e:
         #   print "%s %s" % (specimen, e)
    col_notes = b.CollectionNotes
    dis_notes = b.dissections_set.get().Notes
    #except ObjectDoesNotExist as e:
     #   logging.warn('specimen %s %s' % (specimen, e))
    #except Exception as e:
     #   logging.warn('another exception happened: %s' % e)
    #print "%s %s" % (specimen, weight)
        #pass
    #print size
    row = [
        specimen,
        species,
        sci_name,
        fg,
        #size,
        weight,
        col_notes,
        dis_notes
        ]

### C ###
# 4 - get fish that do have 'NA' samples but which have not been packed
packed = PackedSamples.objects.select_related() \
    .distinct('fk_Sample__fk_Specimen')

# gets fish specimens that have 'NA' samples:
na_fish = fish.filter(samples__in=na_samples)

C = na_fish.exclude(samples__packedsamples__in=packed)
print '> Specimens have "NA" samples but which have not been packed yet: %s' % \
C.count()

row = [
    'SpecimenID',
    'SampleID'
    'SpeciesCode',
    'ScientificName',
    'Fg',
    'SizeClass',
    'Weight',
    'CollectionNotes',
    'DissectionNotes',
    'SampleNotes',
    'PackingNotes'
    ]

writer.writerow('')
writer.writerow(['Fish that have NA samples but which have not been packed'])
writer.writerow(row)

for c in C:
    specimen = c.SpecimenID
    try:
        sample = c.samples_set.get().SampleID
    except MultipleObjectsReturned as e:
        logging.warn("%s for specimen %s" % (e, specimen))
        sample_list = c.samples_set.all().values_list('SampleID', flat=True)
        sample = ', '.join(sample_list)
    species = c.fk_Species.SpeciesCode
    sci_name = c.fk_Species.ScientificName
    fg = c.fk_Species.fk_Guild.GuildCode
    size = c.dissections_set.get().SizeClass()
    weight = c.dissections_set.get().wt
    try:
        spec_notes = c.CollectionNotes
    except AttributeError as e:
        logging.warn("%s has no notes (%s)" % (specimen, e))
        spec_notes = 'None'
    dis_notes = c.dissections_set.get().Notes
    try:
        samp_notes = c.samples_set.get().Notes
    except ObjectDoesNotExist as e:
        logging.warn("%s has no notes (%s)" % (specimen, e))
        samp_notes = 'None'
    except MultipleObjectsReturned as e:
        logging.warn("%s has %s" % (specimen, e))
        samp_notes = "Separate notes for each sample, check sample notes manually"
        
    row = [
        specimen,
        sample,
        species,
        sci_name,
        fg,
        size,
        weight,
        spec_notes,
        dis_notes,
        samp_notes
        ]  

    writer.writerow(row)


### D ###
# 5 - get fish that have packed 'NA' samples but which have not yet been 
# submitted
# gets packed 'NA' samples that do not yet have results:
results = Results.objects.all()
na_packed = na_samples.filter(packedsamples__in=packed)

no_results = na_samples.exclude(packedsamples__in=results)

na_not_submit = na_samples.filter(packedsamples__fk_TrayName__Submitted=False)

not_submitted = na_samples.filter(packedsamples__fk_TrayName__Submitted=False)

no_results = na_samples.exclude(packedsamples__in=results)

# get packed 'NA' samples that do not have any results:


for not_submit in na_not_submit:
    sample = not_submit.SampleID
    tray_list = not_submit.packedsamples_set.all() \
    .values_list('fk_TrayName__TrayName', flat=True)
    trays = ', '.join(tray_list)
    

D = C.filter(samples__in=na_submitted).exclude(samples__in=have_results)
 # packed NA samples not yet submitted and for which no results exists 

row = [
    'Tray',
    'SpecimenID',
    'SpeciesCode',
    'ScientificName',
    'Fg',
    'SizeClass',
    'Weight',
    'CollectionNotes',
    'DissectionNotes',
    'SampleNotes',
    'PackingNotes',
    'TrayNotes'
    ]

writer.writerow('')
writer.writerow(['Fish with NA samples that have been packed but not submitted'])
writer.writerow(row)

for d in D:
    try:
        tray = b.samples_set.packed_set.get().fk_TrayName__TrayName
        specimen = b.SpecimenID
        species = b.fk_Species.SpeciesCode
        sci_name = b.fk_Species.ScientificName
        fg = b.fk_Species.fk_Guild.GuildCode
        size = b.dissections_set.get().SizeClass()
        weight = b.dissections_set.get().wt
        spec_notes = b.Notes
        dis_notes = b.dissections_set.get().Notes
        samp_notes = b.samples_set.get().Notes
        pack_notes = b.samples_set.packed_set.get().Notes
        tray_notes = b.samples_set.packed_set.trays_set.get().Notes
    except ObjectDoesNotExist as e:
        logging.warn('specimen %s %s' % (specimen, e))  
        
    row = [
        tray,
        submitted,
        specimen,
        species,
        sci_name,
        fg,
        size,
        weight,
        spec_notes,
        dis_notes,
        samp_notes,
        pack_notes,
        tray_notes
        ]  

    writer.writerow(row)


"""
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
"""










































