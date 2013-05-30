import os
import csv
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q, Count

from fishdb import settings
from apps.data.models import *
from apps.species.models import *

date = datetime.now().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')

filename = "spp_cnt_for_AnimalCare_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

row = ['Breakdown of species collected in 2012 for Animal Care report.']
writer.writerow(row)
row = ['Report generated on %s by JD' % date_y] 
writer.writerow(row)
writer.writerow([''])

row = [
    'Species Code',
    'Scientific Name',
    'Count'
    ]
writer.writerow(row)

kif12 = Specimens.objects.select_related().filter(SpecimenID__contains='KIF12')
fish_2012 = kif12.filter(fk_Species__fk_Type__Type='fish').distinct()
by_spp = fish_2012.values('fk_Species__SpeciesCode')
spp_cnt = by_spp.annotate(cnt=Count('fk_Species__SpeciesCode'))

for i in range(0, spp_cnt.count()):
    spp = spp_cnt[i]['fk_Species__SpeciesCode']
    count = spp_cnt[i]['cnt']
    sci_name = Species.objects.filter(SpeciesCode=spp).get().ScientificName
    print " > %s - %s: %s" % (spp, sci_name, count)

    row = [
        spp,
        sci_name,
        count
    ]

    writer.writerow(row)
