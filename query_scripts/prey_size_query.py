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

filename = "dissection_data_for_prey_size%s.csv" % dt_now

with open(filename, 'wb') as open_file:
    writer = csv.writer(open_file, dialect='excel')
    row = [
        "Type",
        "SpecimenID",
        "SpeciesCode",
        "Family",
        "FunctionalGroup",
        "SiteName",
        "SizeClass",
        "wt",
        "SL",
        "gh",
        "gw",
        "TL",
        "FL",
        "DissectedBy",
        "CollectionNotes",
        "StomachSample",
        "StomachContents",
        "PreySize",
        "DissectionNotes"
        ]

    writer.writerow(row)

    ds = Dissections.objects.select_related().all()

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
        gh = d.gh or ''
        gw = d.gw or ''
        TL = d.TL
        FL = d.FL
        by = d.DissectedBy
        d_notes = d.Notes
        stomCont = d.StomachContents
        stomSamp = d.StomachSample
        Type = d.fk_Specimen.fk_Species.fk_Type.Type
        
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
            gh,
            gw,
            TL,
            FL,
            by,
            c_notes,
            stomSamp,
            stomCont,
            psize,
            d_notes
        ]

#        writer.writerow(row)

        writer.writerow([unicode(s).encode("utf-8") for s in row])


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