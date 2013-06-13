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

date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')


filename = "funnel_list_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

writer.writerow(['List of specimens that do not have results because they have not progressed through the entire processing chain.'])
writer.writerow([''])


# 1 - select ALL fish specimens:
# and exclude the CHRMAR CW samples that were lost from the Stanford freezer
fish = Specimens.objects.select_related().filter(
    fk_Species__fk_Type__Type='fish').exclude(
    CollectionNotes__contains='all samples for Chromis margaritifer were lost from the Stanford freezer')

### A ### - Dissections are probably needed:
# 2 - get all of the fish that have no samples
samples = Samples.objects.select_related().all()

A = fish.exclude(samples__in=samples).distinct('SpecimenID')

writer.writerow(['Specimens that have NO samples and likely have not been dissected'])
writer.writerow([''])

row = [
    "specimenID",
    "species",
    "sci_name",
    "site",
    "fg",
    "size",
    "weight",
    "stomach_sample",
    "dissection",
    "collection_notes",
    "dissection_notes"
    ]
writer.writerow(row)

for a in A:
    specimen = a.SpecimenID
    species = a.fk_Species.SpeciesCode
    sci_name = a.fk_Species.ScientificName
    fg = a.fk_Species.fk_Guild.GuildCode
    site = a.fk_Site.SiteName

    spec_notes = a.CollectionNotes
    try:
        if a.dissections_set.get().id:
            dis = 'true'
        size = a.dissections_set.get().SizeClass()
        weight = a.dissections_set.get().wt
        stomach = a.dissections_set.get().StomachSample
        dis_notes = a.dissections_set.get().Notes

    except ObjectDoesNotExist as e:
        logging.warn('%s has no dissection data')
        dis = 'false'
        size = "specimen not dissected"
        weight = "specimen not dissected"
        stomach = "specimen not dissected"
        dis_notes = "specimen not dissected"

    row = [
        specimen,
        species,
        sci_name,
        site,
        fg,
        size,
        weight,
        stomach,
        dis,
        spec_notes,
        dis_notes
        ]

    writer.writerow(row)


### B ### - Will need washing/drying:
# 3 - get all of the specimens that have no 'NA' samples but have probably been 
# dissected

na_samp = Samples.objects.filter(
    preprocessings__fk_Treatment__TreatmentCode='NA')

no_na = fish.exclude(samples__in=na_samp).exclude(id__in=A).distinct('id')

B = no_na

writer.writerow([''])
writer.writerow(['List of specimens that need "NA" samples made'])
writer.writerow([''])
row = [
    "specimenID",
    "species",
    "sci_name",
    "fg",
    "site",
    "size",
    "weight",
    "stomach_sample",
    "collection_notes",
    "dissection_notes"
    ]
writer.writerow([''])
writer.writerow(row)

for b in B:
    specimen = b.SpecimenID
    species = b.fk_Species.SpeciesCode
    sci_name = b.fk_Species.ScientificName
    site = b.fk_Site.SiteName
    
    try:
        fg = b.fk_Species.fk_Guild.GuildCode
    except AttributeError as e:
        logging.warn("%s %s" % (specimen, e))
        fg = "no functional group assigned to %s" % species

    size = b.dissections_set.get().SizeClass()
    weight = b.dissections_set.get().wt
    stomach_sample = b.dissections_set.get().StomachSample
    col_notes = b.CollectionNotes
    dis_notes = b.dissections_set.get().Notes

    row = [
        specimen,
        species,
        sci_name,
        fg,
        site,
        size,
        weight,
        stomach_sample,
        col_notes,
        dis_notes
        ]
    try:
        writer.writerow(row)
    except UnicodeEncodeError as e:
        logging.warn("%s %s" % (specimen, e))

### C ###
# 4 - get fish that do have 'NA' samples but which have not been packed

packed = PackedSamples.objects.select_related().all()

# gets all NA fish samples
na_fish = fish.filter(samples__in=na_samp)

not_packed = na_fish.exclude(samples__packedsamples__in=packed).distinct('id')

C = not_packed

writer.writerow([''])
writer.writerow(['List of specimens that need "NA" samples to be packed'])
writer.writerow([''])
row = [
    "specimenID",
    "sampleID",
    "species",
    "sci_name",
    "fg",
    "site",
    "size",
    "weight",
    "stomach_sample",
    "collection_notes",
    "dissection_notes",
    "sample_notes",
    "prep_notes"
    ]
writer.writerow([''])
writer.writerow(row)


for c in C:
    specimen = c.SpecimenID
    samples = c.samples_set.all().values_list('SampleID', flat=True)
    sample = ', '.join(samples)
    species = c.fk_Species.SpeciesCode
    sci_name = c.fk_Species.ScientificName
    site = c.fk_Site.SiteName

    try:
        fg = c.fk_Species.fk_Guild.GuildCode
    except AttributeError as e:
        logging.warn("%s %s" % (specimen, e))
        fg = "no functional group assigned to %s" % species

    size = c.dissections_set.get().SizeClass()
    weight = c.dissections_set.get().wt
    stomach_sample = c.dissections_set.get().StomachSample

    col_notes = c.CollectionNotes
    dis_notes = c.dissections_set.get().Notes
    try:
        samp_notes = c.samples_set.get().Notes
    except MultipleObjectsReturned as e:
        try:
            s_note_list = c.samples_set.all().values_list('Notes', flat=True)
            samp_notes = ', '.join(s_note_list)
        except TypeError as e:
            logging.warn("%s" % e)
            samp_notes = "manually check notes"
    try:
        prep_note_list = c.samples_set.get().preprocessings_set.all() \
            .values_list('Notes', flat=True)
        prep_notes = ', '.join(prep_note_list)
    except MultipleObjectsReturned as e:
        try:
            for s in c.samples_set.all():
                prep_note_list = s.preprocessings_set.all().values_list(
                    'Notes', flat=True)
                prep_notes = ', '.join(prep_note_list)
        except TypeError as e:
            logging.warn("%s" % e)
            prep_notes = "manually check notes"

    row = [
        specimen,
        sample,
        species,
        sci_name,
        fg,
        site,

        size,
        weight,
        stomach_sample,

        col_notes,
        dis_notes,
        samp_notes,
        prep_notes
    ]
    writer.writerow(row)


### D ###
# 5 - get fish that have packed 'NA' samples but which have not yet been 
# submitted and for which NO results exist
submit = packed.filter(fk_TrayName__Submitted=True)
results = Results.objects.select_related().all()

na_packed = na_fish.filter(samples__packedsamples__in=packed)

need_submit = na_packed.exclude(samples__packedsamples__results__in=results) \
    .exclude(samples__packedsamples__in=submit)

D = need_submit


writer.writerow([''])
writer.writerow(['List of specimens that have packed "NA" but need to be submitted'])
writer.writerow([''])

row = [
    "specimenID",
    "sampleID",
    "species",
    "sci_name",
    "fg",
    "site",

    "tray",
    "tray_position",

    "size",
    "weight",
    "stomach_sample",
    "collection_notes",
    "dissection_notes",
    "sample_notes",
    "prep_notes",
    "packed_notes"
    ]
writer.writerow([''])
writer.writerow(row)

for d in D:
    specimen = d.SpecimenID
    samples = d.samples_set.all().values_list('SampleID', flat=True)
    sample = ', '.join(samples)
    species = d.fk_Species.SpeciesCode
    sci_name = d.fk_Species.ScientificName
    site = d.fk_Site.SiteName
    try:
        ps = d.samples_set.get().packedsamples_set.get().fk_Sample.SampleID    
        #ps_list = d.samples_set.get().packed_samples.all() \
        #    .values_list('fk_Sample__SampleID', flat=True)
        #ps = ', '.join(ps_list)
    except MultipleObjectsReturned as e:
        try:
            for s in d.samples_set.get():
                ps_list = s.packedsamples_set.all() \
                    .values_list('fk_SampleID__SampleID')
                ps = ', '.join(ps_list)
        except MultipleObjectsReturned as e:
            ps = "see SampleIDs listed"
    try:
        tray = ps.get().fk_TrayName.TrayName
        trow = ps.get().TrayRow
        tcol = ps.get().TrayColumn
        position = trow + tcol
    except AttributeError as e:
        tray = "look up tray manually"
        position = "check position manually"
    try:
        fg = d.fk_Species.fk_Guild.GuildCode
    except AttributeError as e:
        logging.warn("%s %s" % (specimen, e))
        fg = "no functional group assigned to %s" % species

    size = d.dissections_set.get().SizeClass()
    weight = d.dissections_set.get().wt
    stomach_sample = d.dissections_set.get().StomachSample

    col_notes = d.CollectionNotes
    dis_notes = d.dissections_set.get().Notes
    try:
        s_note_list = d.samples_set.all().values_list('Notes', flat=True)
        samp_notes = ', '.join(s_note_list)
    except TypeError as e:
        logging.warn("%s" % e)
        samp_notes = "manually check notes"
    try:
        prep_note_list = d.samples_set.get().preprocessings_set.all() \
            .values_list('Notes', flat=True)
        prep_notes = ', '.join(prep_note_list)
    except MultipleObjectsReturned as e:
        try:
            for s in d.samples_set.all():
                prep_note_list = s.preprocessings_set.all().values_list(
                    'Notes', flat=True)
                prep_notes = ', '.join(prep_note_list)
        except TypeError as e:
            logging.warn("%s" % e)
            prep_notes = "manually check notes"
    try:
        packed_notes = d.samples_set.get().packedsamples_set.get().Notes
    except MultipleObjectsReturned as e:
        try:
            for s in d.samples_set.all():
                p_list = s.packedsamples_set.all().values_list('Notes', flat=True)
                packed_notes = ', '.join(p_list)
        except TypeError as e:
            packed_notes = "manually check notes"

    row = [
        specimen,
        sample,
        species,
        sci_name,
        fg,
        site,
        tray,
        position,
        size,
        weight,
        stomach_sample,
        col_notes,
        dis_notes,
        samp_notes,
        prep_notes,
        packed_notes
        ]
    writer.writerow(row)



















