#!/usr/bin/env python

import csv
import logging
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist

from fishdb import settings
from apps.data.models import *
from apps.helpers.models import *
from apps.species.models import *

logging.basicConfig(level=logging.INFO)

date = datetime.now().strftime('%b%d')  # 
date_y = datetime.now().strftime('%b %d, %Y')

# Setting up the csv file:
filename = "all_SI_results_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

writer.writerow(['Query script: <fish_SI_results.py>'])
writer.writerow(['Queried by JD on %s' % date_y])
writer.writerow(['All stable isotope results from fish samples that were non-acidified and which had results processed at UCDavis or UVic'])
writer.writerow([''])

# Get all results from the labs UCDavis and UVic:
results = Results.objects.select_related().filter(Lab__in=['UCDavis', 'UVic'])

row = [
    "Sample",
    "Specimen",

    "Species",
    "SciName",
    "Fg",

    "Year",
    "Site",
    "Region",

    "SizeClass",
    "Weight_(g)",
    "TL_(mm)",
    "FL_(mm)",
    "SL_(mm)",

    "Treatment",

    "d13C",
    "d15N",

    "CollectionNotes",
    "DissectionNotes",
    "SampleNotes",
    "PrepNotes",
    "PackedNotes"
    ]

writer.writerow(row)

for r in results:
    samp = r.fk_Packed.fk_Sample
    spec = r.fk_Packed.fk_Sample.fk_Specimen

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

    sp_type = spec.fk_Species.fk_Type.Type

    if sp_type == 'fish':
        try:
            size = spec.dissections_set.get().SizeClass()
            wt = spec.dissections_set.get().wt
            tl = spec.dissections_set.get().TL
            fl = spec.dissections_set.get().FL
            sl = spec.dissections_set.get().SL
            dis_notes = spec.dissections_set.get().Notes
        except ObjectDoesNotExist as e:
            logging.warn("%s %s" % (specimen, e))
    else:
        size = None
        wt = None
        tl = None
        fl = None
        sl = None
        dis_notes = None

    treat = samp.preprocessings_set.get().fk_Treatment.TreatmentCode

    dC13 = r.d13C
    dN15 = r.d15N

    coll_notes = spec.CollectionNotes
    samp_notes = samp.Notes
    prep_notes = samp.preprocessings_set.get().Notes
    packed_notes = r.fk_Packed.Notes

    row = [
        sample,
        specimen,

        species,
        sci_name,
        fg,

        year,
        site,
        fish_prod,

        size,
        wt,
        tl,
        fl,
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




























