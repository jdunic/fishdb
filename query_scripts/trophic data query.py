#!/usr/bin/env python

import os
from django.core.management import setup_environ
from fishdb import settings
setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
from django.db import models
from fishdb.models import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# random python libraries:
import sys
import csv
from datetime import datetime

dt_now = datetime.now().strftime('_%Y_%m_%d')

filename = "tropic_data_test%s.csv" % dt_now

with open(filename, 'wb') as open_file:
    writer = csv.writer(open_file, dialect='excel')
    
    row = [
        "SpecimenID",
        "SampleID",
        "Species Code",
        "Family",
        "Order",
        "Functional Group"
        "Site",
        "Max Length (mm)",
        "Log2 size class",
        "TL (mm)",
        "SL (mm)",
        "Weight (g)",
        "Treatment",
        "Collection notes",
        "Dissection notes",
        "Sample notes",
        "Prep notes",
        "Length weight notes"
        ]

    writer.writerow(row)

    samples = Samples.objects.select_related().all()
    d = Dissections.objects.select_related().all()

    for s in samples:
        specID = s.fk_Specimen
        specimen = s.fk_Specimen.SpecimenID
        sample = s.SampleID
        species = s.fk_Specimen.fk_Species.SpeciesCode
        family = s.fk_Specimen.fk_Species.Family
        order = s.fk_Specimen.fk_Species.Order
        
        if s.fk_Specimen.fk_Species.fk_Guild is None:
            fg = 'NA'
        else:
            fg = s.fk_Specimen.fk_Species.fk_Guild.GuildCode

        site = s.fk_Specimen.fk_Site.SiteName
        maxL = s.fk_Specimen.fk_Species.fk_LengthWeight.fbMaxLen
        treatment = s.fk_

        writer.writerow([unicode(s).encode("utf-8") for s in row])

"""
    for d in ds:
        spec = d.fk_Specimen.SpecimenID
        sp = d.fk_Specimen.fk_Species.SpeciesCode
        fam = d.fk_Specimen.fk_Species.Family
        if d.fk_Specimen.fk_Species.fk_Guild is None:
            fg = 'NA'
        else:
            fg = d.fk_Specimen.fk_Species.fk_Guild.GuildCode
        site = d.fk_Specimen.fk_Site.SiteName
        c_notes = d.fk_Specimen.CollectionNotes
        size = d.SizeClass()
        psize = d.PreySize
        wt = d.wt
        SL = d.SL
        TL = d.TL
        d_notes = d.Notes
        Type = d.fk_Specimen.fk_Species.fk_Type.Type
        sample = 
        row = [
            Type,
            spec,
            sp,
            fam,
            fg,
            site,
            size,
            wt,
            SL,
            TL,
            c_notes,
            psize,
            d_notes
        ]

#        writer.writerow(row)

        writer.writerow([unicode(s).encode("utf-8") for s in row])
"""

"""  writer = csv.writer(response)

    # just any model...
    cars = Car.objects.filter()        

    for car in cars:
        writer.writerow([car.model, car.year])

writer.writerows(User.objects.values_list('id','username','date_joined'))


from django.core.management.base import NoArgsCommand, make_option

class DissectionData(NoArgsCommand):

    help = "Whatever you want to print here"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        ... call your script here ...
Put this in a file, in any of your apps under management/commands/yourcommand.py 
(with empty __init__.py files in each) and now you can call your script with ./manage.py yourcommand.




import csv

filename = "specimen_export%s.csv" % time.time()

writer = csv.writer(open(filename, 'wb'), dialect='excel')

specimens = Specimens.objects.all()
species = Species.objects.all()
sites = Sites.objects.all()
row = [
    "SpecimenID",
    "SpeciesCode",
    "Site"
    ]

writer.writerow(row)
"""