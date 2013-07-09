#!/usr/bin/env python
import os
import csv
#import collections
from datetime import datetime

from django.core.management import setup_environ
from django.db.models import Q

from fishdb import settings
from apps.data.models import *
from apps.helpers.models import *

# setup_environ(settings)

# Looking for fish, SHARK.SP from 2011 and 2012

dt_now = datetime.now().strftime('_%Y_%m_%d')
filename = "BarcodingSampleList%s.csv" % dt_now

writer = csv.writer(open(filename, 'wb'), dialect='excel')
header = ["""This query was made for DNA barcoding purposes and contains all 
fish specimens for 2011 and 2012"""]
writer.writerow(header)
row = [
		"SpecimenID", 
		"Date",
		"Site",
		"Species",
		"ProdFish",
		"Notes"
	]
writer.writerow(row)

fishes = Specimens.objects.filter(
	Q(DateCollected__year='2011') | Q(DateCollected__year='2012')
	).filter(
	fk_Species__fk_Type__Type='fish'
	).order_by(
	'fk_Species__SpeciesCode', 'fk_Site__ProdFish', 'fk_Site__SiteName', 
	'DateCollected'
	)

for fish in fishes:
	specimenID = fish.SpecimenID
	date = fish.DateCollected
	site = fish.fk_Site.SiteName
	species = fish.fk_Species.SpeciesCode
	prodfish = fish.fk_Site.ProdFish
	notes = fish.CollectionNotes

# uniquesites = sitelist.distinct('fk_Site__SiteName')
	
	row = [specimenID, 
		   date,
		   site,
		   species,
		   prodfish,
		   notes
		 ]
	writer.writerow(row)

newfilename = "BarcodingSpeciesListSites%s.csv" %dt_now
newwriter = csv.writer(open(newfilename, 'wb'), dialect='excel')

header = ["""This is a list of unique fish species from the 2011 and 2012 
sampling seasons for use in DNA barcoding."""]
newwriter.writerow(header)

row = [
	"SpeciesCode",
	"ScientificName",
		]
newwriter.writerow(row)



species_list = fishes.order_by(
	'fk_Species__SpeciesCode'
	).distinct(
	'fk_Species__SpeciesCode'
	)

for sp in species_list:
	spcode = sp.fk_Species.SpeciesCode
	sciname = sp.fk_Species.ScientificName
	#print spcode + "\t" + sciname
	"""filtered = fishes.filter(fk_Species__SpeciesCode = spcode
		).order_by(
		'fk_Site__SiteName'
		).distinct(
		'fk_Site__SiteName'
		)
	row = [spcode,
		   sciname]
	newwriter.writerow(row)""" # Only needed for site specific information

	for site in filtered:
		uniquesite = site.fk_Site.SiteName
		siterow = [uniquesite
				   ]
		newwriter.writerow(siterow)
	




"""	row = [spcode,
		   sciname,
		   uniquesite
		   ]
	newwriter.writerow(row)"""


"""SELECT DISTINCT species 
FROM fishes"""

