#!/usr/bin/env python

# good coding practice restricts line length to 80 characters
# python generally uses '_' to separate words in variable names (not periods!)

# python imports:
import csv
import os
import logging
from datetime import datetime

# django imports:
from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

# importing django settings and the necessary database models:
from fishdb import settings
from apps.data.models import *
from apps.helpers.models import *
from apps.sharks.models import *
from apps.species.models import *

# Setting the Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

# Enabling error logging for Python and Django exceptions (mainly what I use it
# for).
logging.basicConfig(level=logging.INFO)

# Making some dates (gets today's date) and formatting to use in filenames and
# file headers.  See python docs for strftime options
date = datetime.now().strftime('%b%d')  # 
date_y = datetime.now().strftime('%b %d, %Y')

# Setting up the csv file:
filename = "shark_data_SI_export_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')


row = ["Shark SI results as of %s" % date_y]
writer.writerow(row) 
writer.writerow([''])

row = [
    "sampleID",
    "tray",
    "specimenID",
    "species_code",
    "sci_name",
    "site",
    "piece",
    "tissue type",
    "treatment",
    "dC13",
    "dN15",
    "fk_HHS",
    "sample_notes",
    "collection_notes",
    "packing_notes"
    ]
writer.writerow(row)

# The following query will get all the shark samples and associated metadata for
# which we have results.

# From all samples get a queryset containing only shark samples:
#shark_samples = Samples.objects.select_related() \
 #   .filter(fk_Specimen__fk_Species__fk_Type__Type='shark')

shark_samples = SharkSamples.objects.select_related()

print shark_samples[0]

# From all results get a queryset containing only shark sample results and
# order by SampleID
results = Results.objects.select_related() \
    .filter(fk_Packed__fk_Sample__sharksamples__in=shark_samples)

packed = PackedSamples.objects.select_related() \
    .filter(fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='shark')

# For each result in the results queryset get the information that you need:
for result in results:
    s = result.fk_Packed.fk_Sample

    specimen = s.fk_Specimen.SpecimenID
    species = s.fk_Specimen.fk_Species.SpeciesCode
    sci_name = s.fk_Specimen.fk_Species.ScientificName
    site = s.fk_Specimen.fk_Site.SiteName

    sample = result.fk_Packed.fk_Sample.SampleID

    stype = s.fk_SampleType.SampleType
    try:
        piece = s.sharksamples_set.get().fk_SharkPiece.SharkPiece
        treatment = s.sharksamples_set.get().fk_State.State
    except ObjectDoesNotExist as e:
        logging.warn("sample %s %s" % (sample, e))
        piece = "no shark %s in SharkSamples" % sample
        treatment = "no shark %s in SharkSamples" % sample
    
    samp_notes = s.Notes
    coll_notes = s.fk_Specimen.CollectionNotes
    pack_notes = result.fk_Packed.Notes
    
    C13 = result.d13C
    N15 = result.d15N
    
    tray = result.fk_Packed.fk_TrayName.TrayName

    # Need to use 'try:' and 'except' because not all samples in results has an
    # associated HHS. This allows me to get the HHS id (primary key) for the 
    # samples that DO have an associated HHS and for those that do not a note
    # will explicitly tell you in the csv report.
    try:
        fk_HHS = s.fk_Specimen.sharkhhsjoins_set.get().fk_HHS.id
    except ObjectDoesNotExist as e:
        #logging.warn("sample %s %s" % (s.id, e))  # prints an error message in
                                                  # the terminal for reference
        fk_HHS = 'no HSS associated with this shark'
    except MultipleObjectsReturned as e:
        logging.warn("specimen %s %s" % (specimen, e))
        fk_HHS = 'needs to have only 1 HHS associated with the specimen'
        # NEED TO FIX THIS. Need to make it so that each specimen only has one
        # HHS associated with it. See KIR2012 - filtering, outreach, surveys.csv
        # and make the necessary correction.

    row = [
        sample,
        tray,
        specimen,
        species,
        sci_name,
        site,
        piece,
        stype,
        treatment,
        C13,
        N15,
        fk_HHS,
        samp_notes,
        coll_notes,
        pack_notes
        ]
 
    writer.writerow(row)  # writes the row defined in row = [...] into the csv
                          # file defined as filename for each iteration through
                          # the 'results' queryset.


filename = "shark_HHS_data_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')


row = ["HHS information that can be matched with the fk_HHS column in <shark_data_SI_export_%s.csv> in R if you want" % date] 
writer.writerow(row) 
writer.writerow([''])

row = [
    "pk_HHS",
    "names",
    "village",
    "fishing_location",
    "date_surveyed"
    ]
writer.writerow(row)

hhs = HHS.objects.all()

for survey in hhs:
    pk = survey.id
    names = survey.Names
    village = survey.Village
    fishing = survey.FishingLocation
    date = survey.DateSurveyed

    row = [
        pk,
        names,
        village,
        fishing,
        date
        ]

    writer.writerow(row)




