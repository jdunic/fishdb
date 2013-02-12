"""
git add -A
then type
git commit -m "updates"
then type
git push
"""

"""
source venv/bin/activate
"""

# setup django
from django.core.management import setup_environ
from fishdb import settings
from datetime import datetime
from decimal import Decimal

setup_environ(settings)

import csv

#from django.core.management import setup_environ
from fishdb.models import *
#from fishdb import settings

#setup_environ(settings)

def cm_import():
	filename = 'csv_data/CollectionMethods.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			method = row['CollectionMethod']
			print method
			cm, created = CollectionMethods.objects.get_or_create(
				Method=method
			)
			# "cm, created" tells django to put the object first, then boolean 
			# for created in that order: (obj, T/F) 
			# get_or_create returns a tuple of the object created or 
			# retrieved and whether it was created or retrieved.
			# therefore I have to save only the object of the tuple if
			# it was actually created:

			if created:
				#cm.Method=method  # not necessary because we already 
				# told it Method=method in the 'cm, created = ...'
				cm.save()
		
def fh_import():
	filename = 'csv_data/FishingHabitats.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			fmp_habitatID = row['pk_FishingHabitatID']
			habitat = row['FishingHabitat']

			habs, created = FishingHabitats.objects.get_or_create(
				fmp_habitat = fmp_habitatID,
				Habitat = habitat
			)

			if created:
				habs.save()

def fm_import():	
	filename = 'csv_data/FishingMethods.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
				fmp_methodID = row['pk_FishingMethodID']
				method = row['FishingMethod']

				meths, created = FishingMethods.objects.get_or_create(
					fmp_methodID = fmp_methodID,
					Method = method
				)

				if created:
					meths.save()

def wp_import():
	filename = 'csv_data/Waypoints.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			lat = row['Latitude']
			longit = row['Longitude']
			notes = row['Notes']
			SiteNum = row['SiteNo']
			wp = row['Waypoint']
			year = row['YearGroundTruthed']

			yeard = None
			if year != '':
				yeard = datetime.strptime(year, '%Y-%m-%d').date()

			wps, created = Waypoints.objects.get_or_create(
				Waypoint=wp,
				Latitude=lat,
				Longitude=longit,
				Notes=notes,
				Year=yeard,
				SiteNum=SiteNum
			)
			
			if created:
				wps.save()

def fg_import():
	filename = 'csv_data/FunctionalGroups.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			fmp_guildID = row['pk_GuildID']
			code = row['GuildCode']
			guild = row['GuildName']

			g, created = FunctionalGroups.objects.get_or_create(
				GuildName = guild,
				GuildCode = code,
				fmp_guildID = fmp_guildID
			)
			
			if created:
				g.save()

def lw_import():
	filename = 'csv_data/LengthWeights.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			date = row['DateUpdated']
			fb_maxL = row['FishBaseMaxLength']
			fb_maxRef = row['FishbaseMaxLengthRef']
			fb_Ltype = row['FishbaseMaxLengthType']
			LtoMeas = row['LengthToMeasure']
			locale = row['Locale']
			modelSp = row['ModelSpecies']
			notes = row['Notes']
			parA = row['ParameterA']
			parB = row['ParameterB']
			fmp_LWid = row['pk_LengthWeightID']
			source = row['Sources']
			spp = row['SpeciesCode']

		# Putting date in datetime format:
			dated = datetime.strptime(date, '%Y-%m-%d').date()

		# Putting number strings into decimals (and watching out for NULLS!!!!):
			
			if fb_maxL == '':
				fb_L = None
			else:
				fb_L = Decimal(fb_maxL)
			
			if parA == '':
				A = None
			else: 
				A = Decimal(parA)
			
			if parB == '':
				B = None
			else:
				B = Decimal(parB)

			lw, created = LengthWeights.objects.get_or_create(
				ModelSpecies = modelSp,
				Sources = source,
				ParameterA = A,
				ParameterB = B,
				fbMaxLen = fb_L,
				fbMaxLenType = fb_Ltype,
				fbMaxRef = fb_maxRef,
				Notes = notes,
				DateUpdated = dated,
				SpeciesCode = spp,
				LengthToMeas = LtoMeas,
				Locale = locale,
				fmp_LWid = fmp_LWid
			)

			if created:
				lw.save()

""" I am so confused. The first answer I found was closed because it was too
vague, and the solution to the second one was to do "instance, created = Models.objects..." which I am already doing.

My error is: TypeError: int() argument must be a string or a number, not
'tuple'

And is being set off by:   File "csvimport.py", line 246, in sp_import
fmp_pk=fmp_pk

I double checked that at least before trying to save fmp_pk to my Species
table, that fmp_pk was not a tuple. I'm assuming that it is being turned into a tuple when I do the get_or_create, but I just have no idea how to correct for that.
"""

def sp_import():
	filename = 'csv_data/Taxonomies.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			EnglishName = row['EnglishName']
			family = row['Family']
			fmp_guild = row['fk_GuildID']
			fmp_lw = row['fk_LengthWeightID']
			genus = row['Genus']
			LocalName = row['LocalName']
			notes = row['Notes']
			order = row['Order']
			fmp_speciesID = row['pk_SpeciesID']
			SciName = row['ScientificName']
			code = row['SpeciesCode']

		# make shit an int... IF not ''
			if fmp_speciesID == '':
				fmp_pk = None
			if fmp_speciesID is None:
				fmp_pk = None
			else:
				fmp_pk = int(fmp_speciesID)

			if fmp_guild == '':
				guild1 = None
			else:
				guild1 = int(fmp_guild)
			if fmp_lw == '':
				lw1 = None
			else:
				lw1 = int(fmp_lw)

		# FK lookups:
			if guild1 is not None:
				guild = FunctionalGroups.objects.get_or_create(fmp_guildID=guild1)
			
			if lw1 is not None:
				lw = LengthWeights.objects.get_or_create(fmp_LWid=lw1)

			if isinstance(fmp_pk, tuple) == True:
				print fmp_speciesID
			
			#print isinstance(fmp_speciesID, int)

		# assigning values:
			spp, created = Species.objects.get_or_create(
				ScientificName=SciName,
				Order=order,
				Family=family,
				Genus=genus,
				LocalName=LocalName,
				EnglishName=EnglishName,
				SpeciesCode=code,
				Notes=notes,
				fk_Guild=guild,
				fk_LengthWeight=lw,
				fmp_pk=fmp_pk
			)

			if isinstance(fmp_pk, tuple) ==True:
				print 'bullshit'

			#print Species.objects.fmp_pk()
#			if created:
#				spp.save()


def sites_import():
	filename = 'csv_data/Sites.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			boat = row['BoatAccessibility']
			ProdFish = row['CombinedFishingProductivity']
			notes = row['DescriptiveNotes']
			FishRank = row['FishingLevel']
			IslandArea = row['IslandArea']
			Latitude = row['Latitude']
			Longitude = row['Longitude']
			fmp_siteID = row['pk_SiteID']
			RTCW_Fishing = row['RTCW_6_LevelFishing']
			ShoreEntry = row['ShoreEntry']
			SiteName = row['SiteName']
			SMWfishing = row['SMW_FishingPressure']
			SMWprod = row['SMW_Productivity']
			SMWregion = row['SMW_Region']
			TransitTime = row['TransitTime']

			sts, created = Sites.objects.get_or_create(
				SiteName=SiteName,
				Latitude=Latitude,
				Longitude=Longitude,
				IslandArea=IslandArea,
				ProdFish=ProdFish,
				BoatAccessibility=boat,
				ShoreEntry=ShoreEntry,
				RTCW_Fishing=RTCW_Fishing,
				FishRank=FishRank,
				TransitTime=TransitTime,
				SMWregion=SMWregion,
				SMWprod=SMWprod,
				SMWfishing=SMWfishing,
				Notes=notes,
				fmp_pk=fmp_siteID
			)

			if created:
				sts.save()

def loc_import():
	filename = 'csv_data/Locations.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			name = row['ContainerName']
			ctype = row['ContainerType']
			inst = row['Institution']
			fmp_locationID = row['pk_Location']

			loc, created = Locations.objects.get_or_create(
				ContainerType = ctype,
				ContainerName = name,
				Institution = inst,
				fmp_locationID = fmp_locationID
			)
			
			if created:
				loc.save()

def hhs_import():
	filename = 'csv_data/HHS.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			date = row['DateSurveyed']
			name = row['Names']
			fmp_hhsID = row['pk_hhsID']
			fishing = row['TypicalFishingLocation']
			village = row['Village']

			hhs, created = HHS.objects.get_or_create(
				Names = name,
				Village = village,
				FishingLocation = fishing,
				DateSurveyed = date
			)
			if created:
				hhs.save()

def stype_import():
	filename = 'csv_data/SampleTypes.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			pk_SampleTypeID = row['pk_SampleTypeID']
			stype = row['SampleType']
			TypeCode = row['TypeCode']

			st, created = SampleTypes.objects.get_or_create(
				SampleType=stype,
				TypeCode=TypeCode,
				fmp_pk=pk_SampleTypeID
			)

			if created:
				st.save()

def treat_import():
	filename = 'csv_data/Treatments'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			treat = row['Treatment']
			code = row['TreatmentCode']

			treat, created = Treatments.objects.get_or_create(
				Treatment=treat,
				TreatmentCode=code
			)

			if created:
				treat.save()

def trays_import():
	filename = 'csv_data/Trays.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			tray = row['TrayName']

			tr, created = Trays.objects.get_or_create(
				TrayName=tray
			)

			if created:
				tr.save()

def shjoin_import():
	filename = 'csv_data/Species_Habitat_Joins.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			fk_FishingHabitat = row['fk_FishingHabitatID']
			fk_SpeciesID = row['fk_SpeciesID']

		# FK lookups:
			hab = FishingHabitats.objects.get(Habitat=fk_FishingHabitat)
			spp = Species.objects.get(fmp_pk=fk_SpeciesID)

		# assigning values:
			spp.Habitat.add(hab)
			spp.save()

def smjoin_import():
	filename = 'csv_data/Species_Method_Join.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			fk_FishingMethodID = row['fk_FishingMethodID']
			fk_SpeciesID = row['fk_SpeciesID']

		# FK lookups:
			meth = FishingMethods.objects.get_or_create(Method=fk_FishingMethodID)
			spp = Species.objects.get_or_create(fmp_pk=fk_SpeciesID)

		# assigning values:
			spp.Methods.add(meth)
			spp.save()

def spec_import():
	filename = 'csv_data/Specimens.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			CollectedBy = row['CollectedBy']
			CollectionNotes = row['Collection Notes']
			CollectionMethod = row['CollectionMethod']
			DateCollected = row['DateCollected']
			DateEntered = row['DateEntered']
			DepthCollected = row['DepthCollected']
			fmp_siteID = row['fk_SiteID']
			fmp_speciesID = row['fk_SpeciesID']
			OldID1 = row['OldID1']
			fmp_specimenID = row['pk_SpecimenID']
			sex = row['Sex']
			SpecimenID = row['SpecimenID']

		# FK lookups:
			site = Sites.objects.get_or_create(fmp_pk=fmp_siteID)
			spp = Species.objects.get_or_create(fmp_pk=fmp_speciesID)
			meth = CollectionMethods.objects.get_or_create(Method=CollectionMethod)

		# assigning values:
			spe, created = Specimens.objects.get_or_create(
				fk_Site=site,
				fk_Species=spp,
				fk_Method=meth,
				SpecimenID=SpecimenID,
				CollectedBy=CollectedBy,
				Sex=sex,
				OldID1=OldID1,
				DateEntered=DateEntered,
				CollectionNotes=CollectionNotes,
				DateCollected=DateCollected,
				DepthCollected=DepthCollected,
				fmp_pk=fmp_specimenID
			)

			if created:
				spe.save()

def dis_import():
	filename = 'csv_data/Dissections.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			fmp_specimen_id = row['fk_SpecimenID']
			# get specimen here
			specimen = Specimens.objects.get_or_create(fmp_pk=fmp_specimen_id)

			DateDissected = row['DateDissected']
			DateEntered = row['DateEntered']
			DissectedBy = row['DissectedBy']
			fl = row['FLMM']
			gh = row['gh']
			gonads = row['GonadsRipe']
			gw = row['gw']
			isotope = row['IsotopeSample']
			notes = row['Notes']
			oto = row['OtolithSample']
			photo = row['PhotoFileName']
			PreySize = row['PreySizeInStomach']
			sl = row['SLMM']
			stomach_contents = row['StomachContents']
			stomach_sample = row['StomachSample']
			tl = row['TLMM']
			wt = row['wt']
			dis, created = Dissections.objects.get_or_create(
				fk_Specimen = specimen,
				TL=tl,
				FL=fl,
				SL=sl,
				wt=wt,
				gh=gh,
				gw=gw,
				DateDissected=DateDissected,
				DateEntered=DateEntered,
				StomachContents=stomach_contents,
				PreySize=PreySize,
				StomachSample=stomach_sample,
				IsotopeSample=isotope,
				OtolithSample=oto,
				GonadsRipe=gonads,
				PhotoName=photo,
				DissectedBy=DissectedBy,
				Notes=notes
			)

			if created:
				dis.save()

def samp_import():
	filename = 'csv_data/Samples.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			fmp_specimenID = row['fk_SpecimenID']
			notes = row['notes']
			fmp_pk_samp = row['pk_SampleID']
			ref_type = row['ref_type']
			SampleID = row['SampleID']

		# FK lookup:
			specimen = Specimens.objects.get_or_create(fmp_pk=fmp_specimenID)
			stype = SampleTypes.objects.get_or_create(SampleType=ref_type)

		# assigning values:
			samp, created = Samples.objects.get_or_create(
				fk_Specimen=specimen,
				fk_SampleType=stype,
				SampleID=SampleID,
				Notes=notes,
				fmp_pk=fmp_pk_samp
			)

			if created:
				samp.save()

def state_import():
	filename = 'csv_data/SharkStates.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			State = row['State']

			s, created = SharkStates.objects.get_or_create(
				State=State
			)

			if created:
				s.save()

def piece_import():
	filename = 'csv_data/SharkPieces.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			piece = row['SharkPiece']

		sps, created = SharkPieces.objects.get_or_create(
			SharkPiece=piece
		)

		if created:
			sps.save()

def sharkdis_import():
	filename = 'csv_data/SharkDissections.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			DorsalBase = row['DorsalBase']
			DorsalHeight = row['DorsalHeight']
			fmp_specimenID = row['fk_SpecimenID']
			ForkLength = row['ForkLength']
			notes = row['Notes']
			PectoralBase = row['PectoralBase']
			PectoralHeight = row['PectoralHeight']
			photo = row['PhotoTaken']
			PCL = row['PrecaudLength']
			stretch = row['StretchLength']
			TailBase = row['TailBase']
			TailHeight = row['TailHeight']
			TL = row['TL']
			wt = row['Weight_lbs']
			date = row['DateDissected']

		# Fk lookups:
			specimen = Specimens.objects.get_or_create(fmp_pk=fmp_specimenID)

			sds, created = SharkDissections.objects.get_or_create(
				fk_Specimen=specimen,
				PCL=PCL,
				FL=ForkLength,
				TL=TL,
				stretch=stretch,
				DH=DorsalHeight,
				DB=DorsalBase,
				PH=PectoralHeight,
				PB=PectoralBase,
				TH=TailHeight,
				TB=TailBase,
				wt=wt,
				PhotoTaken=photo,
				Notes=notes,
				DateDissected=date
			)

			if created:
				sds.save()

def sharksamp_import():
	filename = 'csv_data/SharkSamples.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			DateDissected = row['DateDissected']
			notes = row['Notes']
			fmp_hhsID = row['fk_hhsID']
			ref_sampleID = row['ref_SampleID']
			ref_piece = row['ref_sharkpiece']
			ref_state = row['ref_sharkstate']

		# FK lookups:
			hhs = HHS.objects.get_or_create(fmp_pk=fmp_hhsID)
			samp = Samples.objects.get_or_create(Sample=ref_sampleID)
			piece = SharkPieces.objects.get_or_create(SharkPiece=ref_piece)
			state = SharkStates.objects.get_or_create(State=ref_state)

			ss, created = SharkSamples.objects.get_or_create(
				fk_Sample=samp,
				fk_SharkPiece=piece,
				fk_State=state,
				fk_HHS=hhs
			)

			if created:
				ss.save()

def prep_import():
	filename = 'csv_data/Preprocessings.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			DateGround = row['DateGround']
			DateWashed = row['DateWashedDried']
			DryingHours = row['DryingHours']
			method = row['DryingMethod']
			notes = row['Notes']
			fmp_preprocessings = row['pk_PreprocessingID']
			PrepEnteredBy = row['PrepEnteredBy']
			PreppedBy = row['PreppedBy']
			samp = row['ref_SampleID']
			treat = row['ref_treatment']
		
		# FK lookups:
			sample = Samples.objects.get_or_create(SampleID=samp)
			treatment = Treatments.objects.get_or_create(Treatment=treat)

		# assigning values:
			prep, created = Preprocessings.objects.get_or_create(
				fk_Sample=sample,
				fk_Treatment=treatment,
				DateWashDry=DateWashed,
				PreppedBy=PreppedBy,
				PrepEntered=PrepEnteredBy,
				DateGround=DateGround,
				DryingMethod=method,
				DryingTime=DryingHours,
				Notes=notes,
				fmp_preprocessings=fmp_preprocessings
			)

			if created:
				prep.save()

def packed_import():
	filename = 'csv_data/PackedSamples.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			capwt = row['CapsuleWeight']
			DateEntered = row['DateEntered']
			EnteredBy = row['EnteredBy']
			DatePacked = row['DatePacked']
			FilledCapsuleWeight = row['FilledCapsuleWeight']
			notes = row['Notes']
			PackedBy = row['PackedBy']

			sampleID = row['ref_sampleID']
			trayID = row['ref_TrayName']
			wt = row['SampleWeight']
			tcol = row['TrayColumn']
			trow = row['TrayRow']

			fmp_packedID = row['pk_PackedID']
		# FK lookups:
			sample = Samples.objects.get_or_create(SampleID=sampleID)
			tray = Trays.objects.get_or_create(TrayName=TrayName)
		# importing data into table:
			ps, created = PackedSamples.objects.get_or_create(
				fk_Sample = sample,
				fk_TrayName = tray,
				TrayRow = trow,
				TrayColumn = tcol,
				CapWeight = capwt,
				FilledCapWeight = FilledCapsuleWeight,
				SampleWeight = wt,
				PackedBy = PackedBy,
				EnteredBy = EnteredBy,
				DatePacked = DatePacked,
				DateEntered = DateEntered,
				Notes = notes,
				fmp_packedID = fmp_packedID
			)

			if created:
				ps.save()

def result_import():
	filename = 'csv_data/Results.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			d13C = row['d13C']
			d15N = row['d15N']
			DateProcessed = row['DateProcessed']
			Lab = row['Lab']
			fmp_packedID = row['fk_PackedID']
		
		# FK lookups:
			packed = PackedSamples.objects.get_or_create(fmp_packedID=fmp_packedID)

		# assigning values:
			results, created = Results.objects.get_or_create(
				fk_Packed=packed,
				d13C=d13C,
				d15N=d15N,
				Lab=Lab,
				DateProcessed=DateProcessed
			)

			if created:
				results.save()		

def samp_loc_import():
	filename = 'csv_data/SampleLocations.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			DateStatus = row['DateStatusUpdated']
			EnteredBy = row['EnteredBy']
			fmp_location = row['fk_LocationID']
			fmp_sampleID = row['fk_sampleID']
			inst = row['Institution']
			number = row['ref_containNum']
			container = row['ref_containType']

		# FK lookup:
			sample = Samples.objects.get_or_create(fmp_sampleID=fmp_pk)
			loc = Locations.objects.get_or_create(fmp_locationID=fmp_location)

		# assigning values:
			sl, created = SampleLocations.objets.get_or_create(
				fk_Sample=sample,
				fk_Location=loc,
				DateUpdated=DateStatus,
				EnteredBy=EnteredBy,
				Institution=inst
			)

			if created:
				sl.save()

def sss_import():
	filename = 'csv_data/SpecimenSpareSamples.csv'
	with open(filename, 'rU') as csvfile:
		csvreader = csv.DictReader(csvfile)
		for row in csvreader:
			cont = row['Container']
			inst = row['Institution']
			specimenID = row['ref_SpecimenID']

		# FK lookups:
			spec = Specimens.objects.get_or_create(SpecimenID=specimenID)

		# assigning values:
			sss, created = SpecimenSpareSamples.objects.get_or_create(
				fk_Specimen=spec,
				Container=cont,
				Institution=inst,
			)

			if created:
				sss.save()





































































