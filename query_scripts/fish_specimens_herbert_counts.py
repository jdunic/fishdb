#!/usr/bin/env python

import csv
import os
import sys
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count

from fishdb import settings
from apps.data.models import *
from apps.species.models import *
from apps.helpers.models import *

# Setting django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
setup_environ(settings)

date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')

# Creating file
filename = "all_years_fish_specimen_count%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

# Adding query information at top of spreadsheet:
row = ["Number of fish samples for 2010-2012 fish specimens: total and by species"]
writer.writerow(row)
row = ["Original query file: fish_specimens_herbert_counts.py"]
writer.writerow(row)
row = ["Query date: %s, by JD" % date_y] 
writer.writerow([''])

# Count all fish specimens:

fish = Specimens.objects.filter(
    fk_Species__fk_Type__Type = 'fish')

row = [
    "Total count for fish dissections",
    fish.count()
    ]

writer.writerow(row)


# Count number of stomach samples for each functional group:
writer.writerow([''])
writer.writerow(['Fish specimens by species'])

spp_cnt = fish.values('fk_Species__SpeciesCode', 
        'fk_Species__fk_Guild__GuildCode',
        'fk_Species__ScientificName',
        'fk_Species__EnglishName',
        'DateCollected') \
    .annotate(species_count = Count('fk_Species__SpeciesCode'))

num_spp = (spp_cnt.count()-1)
print num_spp

for sp in spp_cnt:
    species = sp['fk_Species__SpeciesCode']
    count = sp['species_count']
    fg = sp['fk_Species__fk_Guild__GuildCode']
    print " > %s, %s: %s" % (species, fg, count)

    row = [
        species,
        fg,
        count
    ]

    writer.writerow(row)



"""

filename = "2011_fish_specimen_count%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

# Adding query information at top of spreadsheet:
row = ["Number of fish samples for 2010: total and by species"]
writer.writerow(row)
row = ["Original query file: fish_specimens_herbert_counts.py"]
writer.writerow(row)
row = ["Query date: %s, by JD" % date_y] 
writer.writerow([''])

# Count all fish specimens:

fish = Specimens.objects.filter(
    fk_Species__fk_Type__Type='fish') \
    .filter(DateCollected__year=2010)

row = [
    "Total count for fish dissections",
    fish.count()
    ]

writer.writerow(row)


# Count number of stomach samples for each functional group:
writer.writerow([''])
writer.writerow(['Fish specimens by species'])

spp_cnt = fish.values('fk_Species__SpeciesCode', 
        'fk_Species__fk_Guild__GuildCode',
        'fk_Species__ScientificName',
        'fk_Species__EnglishName') \
    .annotate(species_count = Count('fk_Species__SpeciesCode'))

num_spp = (spp_cnt.count()-1)
print num_spp

for sp in spp_cnt:
    species = sp['fk_Species__SpeciesCode']
    count = sp['species_count']
    fg = sp['fk_Species__fk_Guild__GuildCode']
    print " > %s, %s: %s" % (species, fg, count)

    row = [
        species,
        fg,
        count
    ]

    writer.writerow(row)
"""




























