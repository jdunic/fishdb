#!/usr/bin/env python

import csv
import logging
from datetime import datetime

from django.db.models import Count

from fishdb import settings
from apps.data.models import *
from apps.species.models import *

logging.basicConfig(level=logging.INFO)

date = datetime.today().strftime('%b%d')
date_y = datetime.now().strftime('%b %d, %Y')

filename = "gape_data_for_MS_%s.csv" % date

writer = csv.writer(open(filename, 'wb'), dialect='excel')

row1 = ["""New fish gape query extracted on %s""" % date_y]
row2 = ["""JD changed FGs to match the classifications in the thesis before
		  running this query."""]
row3 = ["""This output contains specimens that have BOTH gape height and gape
	      width measurements, are fish, and have more than three specimens
	      per species collected"""]
row4 = ['']
writer.writerow(row1)
writer.writerow(row2)
writer.writerow(row3)
writer.writerow(row4)

gapes = Specimens.objects.select_related() \
	.exclude(dissections__gh__isnull=True) \
	.exclude(dissections__gw__isnull=True) \
	.exclude(dissections__SL__isnull=True) 

species = Species.objects.select_related().all() \
	.annotate(num_spec=Count('specimens__SpecimenID')) \
	.filter(num_spec__gt=3) \
	.filter(fk_Type__Type='fish') \
	.filter(specimens__in=gapes)

row = [
	'SpecimenID',
	'Family',
	'Order',
	'Genus',
	'SpeciesCode',
	'j_fg',
	'Site',
	'Region',
	'TL',
	'SL',
	'FL',
	'wt',
	'gh',
	'gw',
	'dissected_by',
	'stomach_contents',
	'prey_size',
	'coll_notes',
	'dis_notes',
	]
writer.writerow(row)

for sp in species:
	spec = sp.specimens_set.all()
	for s in spec:
		specimen_id = s.SpecimenID
		species = s.fk_Species.SpeciesCode
		family = s.fk_Species.Family
		order = s.fk_Species.Order
		genus = s.fk_Species.Genus
		j_fg = s.fk_Species.fk_Guild.GuildCode
		site = s.fk_Site.SiteName
		region = s.fk_Site.ProdFish
		d = s.dissections_set.get()
		tl = d.TL
		fl = d.FL
		sl = d.SL
		wt = d.wt
		gh = d.gh
		gw = d.gw
		dissected_by = d.DissectedBy
		stomach_contents = d.StomachContents
		prey_size = d.PreySize

		coll_notes = s.CollectionNotes
		dis_notes = d.Notes

		row = [
			specimen_id,
			family,
			order,
			genus,
			species,
			j_fg,
			site,
			region,
			tl,
			sl,
			fl,
			wt,
			gh,
			gw,
			dissected_by,
			stomach_contents,
			prey_size,
			coll_notes,
			dis_notes
			]
		try:
			writer.writerow(row)
		except UnicodeEncodeError as e:
			logging.warning("%s %s" % (specimen_id, e))




























