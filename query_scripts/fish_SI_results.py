#!/usr/bin/env python

import csv
import logging
import os
from datetime import datetime

from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist

from fishdb import settings
from apps.data.models import *
from apps.helpers.models import *
from apps.species.models import *

logging.basicConfig(level=logging.INFO)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

date = datetime.now().strftime('%b%d')  # 
date_y = datetime.now().strftime('%b %d, %Y')

# Setting up the csv file:
filename = "fish_SI_results_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

writer.writerow(['Query script: <fish_SI_results.py>'])
writer.writerow(['Queried by JD on %s' % date_y])
writer.writerow(['All stable isotope results from fish samples that were non-acidified and which had results processed at UCDavis or UVic'])
writer.writerow([''])

# Get all results from the labs UCDavis and UVic:
results = Results.objects.select_related().filter(Lab__in=['UCDavis', 'UVic'])
# Get all results for fish samples:
fish = results.filter(
    fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Type__Type='fish')
# Get all results for non-acidified fish samples:
na = fish.filter(
    fk_Packed__fk_Sample__preprocessings__fk_Treatment__TreatmentCode='NA')


row = [
    "sample",
    "specimen",

    "species",
    "sci_name",
    "fg",

    "year",
    "site",
    "fish_prod",

    "weight_(g)",
    "total_length_(mm)",
    "standard_length_(mm)",

    "treatment",

    "d13C",
    "d15N",

    "collection_notes",
    "dissection_notes",
    "sample_notes",
    "prep_notes",
    "packed_notes"
    ]
writer.writerow(row)

for fish in na:
    samp = fish.fk_Packed.fk_Sample
    spec = fish.fk_Packed.fk_Sample.fk_Specimen

    sample = samp.SampleID
    specimen = spec.SpecimenID

    species = spec.fk_Species.SpeciesCode
    sci_name = spec.fk_Species.ScientificName
    try:
        fg = spec.fk_Species.fk_Guild.GuildCode
    #except ObjectDoesNotExist as e:
    except AttributeError as e:
        logging.warn("%s %s" % (species, e))
        fg = "no fg entered for species %s" % species

    year = spec.DateCollected.strftime('%Y')
    site = spec.fk_Site.SiteName
    fish_prod = spec.fk_Site.ProdFish

    wt = spec.dissections_set.get().wt
    tl = spec.dissections_set.get().TL
    sl = spec.dissections_set.get().SL

    treat = samp.preprocessings_set.get().fk_Treatment.TreatmentCode

    dC13 = fish.d13C
    dN15 = fish.d15N

    coll_notes = spec.CollectionNotes
    dis_notes = spec.dissections_set.get().Notes
    samp_notes = samp.Notes
    prep_notes = samp.preprocessings_set.get().Notes
    packed_notes = fish.fk_Packed.Notes

    row = [
        sample,
        specimen,

        species,
        sci_name,
        fg,

        year,
        site,
        fish_prod,

        wt,
        tl,
        sl,

        treat,

        dC13,
        dN15,

        coll_notes,
        dis_notes,
        samp_notes,
        prep_notes,
        packed_notes
        ]

    writer.writerow(row)




























