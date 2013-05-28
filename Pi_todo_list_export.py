#!/usr/bin/env python

import csv
import logging
import os

from django.core.management import setup_environ
from django.db.models import Q, Count
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from fishdb import settings
from fishdb.models import *

# Setting django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.fishdb.settings")
setup_environ(settings)

logging.basicConfig(level=logging.INFO)

# Creating file


filename = "pi_todo_list_May28.csv"

writer = csv.writer(open(filename, 'wb'), dialect='excel')


# Adding query information at top of spreadsheet:
row = ["Piscivore/Apex Predator specimens list. This list can be used to check what Pi/AP specimens need to be processed for stable isotope data"]
writer.writerow(row)
row = ["Original query file: Pi_todo_list_export.py"]
writer.writerow(row)
row = ["Query date: May 27, 2013, by JD"]
writer.writerow(row)

row = [
    "Specimen",
    "Species",
    "Size Class",
    "Stomach y/n",
    "Stomach Contents",
    "Sample1",
    "Treatment1",
    "Packed tray1",
    "Results1 dC13",
    "Results1 dN15",
    "Sample2",
    "Treatment2",
    "Packed tray2",
    "Results2 dC13",
    "Results2 dN15",
    "Sample3",
    "Treatment3",
    "Packed tray3",
    "Results3 dC13",
    "Results3 dN15",
    "Sample4"
    ]

writer.writerow(row)


piscs = Species.objects.select_related().filter( 
    Q(fk_Guild__GuildCode = 'Pi') | Q(fk_Guild__GuildCode = 'AP')).filter(
    )

# Prints a list of Pi/AP species:
for p in piscs:
    spp = piscs.get(SpeciesCode = p)

# All samples of Pi or AP species
samps = Samples.objects.select_related().filter(
    Q(fk_Specimen__fk_Species__fk_Guild__GuildCode = 'Pi') |
    Q(fk_Specimen__fk_Species__fk_Guild__GuildCode = 'AP')
    )

specs = Specimens.objects.select_related().filter(
    Q(fk_Species__fk_Guild__GuildCode = 'Pi') |
    Q(fk_Species__fk_Guild__GuildCode = 'AP')
    )


print specs.count()

line_number = 0

for s in specs:
    line_number += 1
    spec = specs.get(SpecimenID = s)
    spp = spec.fk_Species.SpeciesCode
    try:
        dis = spec.dissections_set.get()
        stom_bool = dis.StomachSample
        stom_cont = dis.StomachContents
        size = dis.SizeClass()

    except ObjectDoesNotExist as e:
        logging.warn("%s, %s" % (spec, e))
        stom_bool = "no dissection data"
        stom_cont = "no data"
        size = "no data"
    #sc = specs.get(SpecimenID = s).SizeClass()
    samps = specs.get(SpecimenID = s).samples_set.all()
    row = [
        spec,
        spp,
        size,
        stom_bool,
        stom_cont
        ]

    for samp in samps:
        try:
            row.append(samp)
            treat = Preprocessings.objects.get(
                fk_Sample__SampleID = samp).fk_Treatment.TreatmentCode

        except ObjectDoesNotExist as e:
            logging.warn("%s treatment %s" % (samp, e))
            treat = "unknown treatment or not in db"
        try:
            packed = PackedSamples.objects.all().filter(
                fk_Sample__SampleID = samp)
            ps = packed.get().fk_TrayName.TrayName
        except ObjectDoesNotExist as e:
            logging.warn("%s not packed" % samp)
            ps = "not packed"
        except MultipleObjectsReturned as e:
            logging.warn("sample %s has %s" % (samp, e))
            ps = "multiple packed samples"
        
        row.append(treat)
        row.append(ps)
        
        try:
            results = Results.objects.all().filter(
                fk_Packed__fk_Sample__SampleID = samp)
            c = results.get().d13C
            n = results.get().d15N

            row.append(c)
            row.append(n)

        except ObjectDoesNotExist as e:
            logging.warn("%s result %s" % (samp, e))
            c = "Result dne"
            n = "Result dne"

            row.append(c)
            row.append(n)

        except MultipleObjectsReturned as e:
            logging.warn("%s result %s" % (samp, e))
            c = "multiple results"
            n = "multiple results"

            row.append(c)
            row.append(n)


            #for r in results:
             #   row.append(r)

            #print ("%s %s" %(samp, treat))


    #except AttributeError as e:
     #   logging.warn("No: %s  Specimen: %s %s" % (line_number, spec, e))

    writer.writerow(row)



















