#!/usr/bin/env python

import csv
import os
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
filename = "stomach_samples_list_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

# Adding query information at top of spreadsheet:
row = ["Stomach sample counts for 2011 and 2012 fish specimens: total, by functional group, and by species"]
writer.writerow(row)
row = ["Original query file: stomach_counts.py"]
writer.writerow(row)
row = ["Query date: %s, by JD" % date_y] 
writer.writerow([''])

# Count all dissected specimens:
fish_d = Dissections.objects.filter(
    fk_Specimen__fk_Species__fk_Type__Type = 'fish')

row = [
    "Total count for fish dissections",
    fish_d.count()
    ]

writer.writerow(row)
writer.writerow('')

# Get dissections with have stomach samples
dis = Dissections.objects.select_related().filter(StomachSample = True)

# Count total number of stomach samples:
cnt_dis = dis.count()
print " > number of stomach samples: %s" % cnt_dis

row = [
    "Total number of stomach samples",
    cnt_dis
    ]

writer.writerow(row)


# Count number of stomach samples for each functional group:
writer.writerow([''])
writer.writerow(['Stomachs by Functional Group'])

guild = 'fk_Specimen__fk_Species__fk_Guild__GuildCode'
fg_cnt = dis.values(guild).annotate(guild_count = Count(guild))

num_fg = (fg_cnt.count()-1)
print num_fg

for fg in fg_cnt:
    count = fg['guild_count']
    fg = fg[guild]
    print " > %s: %s" % (fg, count)

    row = [
        fg,
        count
    ]

    writer.writerow(row)


# Count number of stomach samples for each species:
writer.writerow([''])
writer.writerow(['Stomachs by Species'])

spp = 'fk_Specimen__fk_Species__SpeciesCode'
spp_cnt = dis.values(spp).annotate(spp_count = Count(spp))

num_spp = (spp_cnt.count()-1)
print num_spp

for i in range(0, num_spp):
    count = spp_cnt[i]['spp_count']
    sp = spp_cnt[i][spp]
    print " > %s: %s" % (sp, count)

    row = [
        sp,
        count
        ]

    writer.writerow(row)






























