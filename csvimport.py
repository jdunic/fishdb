# setup django
from django.core.management import setup_environ
from fishdb import settings

setup_environ(settings)

import csv

#from django.core.management import setup_environ
from fishdb.models import *
#from fishdb import settings

#setup_environ(settings)

filename = 'csv_data/CollectionMethods.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		method = row['CollectionMethod']
		cm = CollectionMethods.objects.get_or_create(
			Method=method
		)
		cm.save()
"""
filename = 'csv_data/FishingHabitats.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		fmp_habitatID = row['pk_FishingHabitatID']
		habitat = row['FishingHabitat']

		habs = FishingHabitats.objects.get_or_create(
			fm_habitatID = fm_habitatID,
			Habitat = habitat
		)

		habs.save()

filename = 'csv_data/FishingMethods.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
			fmp_methodID = row['pk_FishingMethodID']
			method = row['FishingMethod']

			meths = FishingMethods.objects.get_or_create(
				fmp_methodID = fmp_methodID,
				Method = method
			)
			meths.save()

filename = 'csv_data/Waypoints.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		lat = row['Latitude']
		longit = row['Longitude']
		notes = row['Notes']
		SiteNum = row['SiteNo']
		wp = row['Waypoint']
		year = row['YearGroundTruthed']

		wps = Waypoints.objects.get_or_create(
			Waypoint=wp,
			Latitude=lat,
			Longitude=longit,
			Notes=notes,
			Year=year,
			SiteNum=SiteNum
		)

		wps.save()

filename = 'csv_data/FunctionalGroups.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		fmp_guildID = row['pk_GuildID']
		code = row['GuildCode']
		guild = row['GuildName']

		guilds = FunctionalGroups.objects.get_or_create(
			GuildName = guild,
			GuildCode = code,
			fmp_guildID = fmp_guildID
		)
		
		guild.save()

filename = 'csv_data/LengthWeights.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		date = row['DateUpdated']
		fb_maxL = row['FishBaseMaxLength']
		fb_maxRef = row['FisbaseMaxLengthRef']
		fb_Ltype = row['FishbaseMaxLengthType']
		LtoMeas = row['LengthToMeasure']
		locale = row['Locale']
		modelSp = row['ModelSpecies']
		notes = row['Notes']
		parA = row['ParameterA']
		parB = row['ParameterB']
		fmp_LWid = row['pk_LengthWeightId']
		source = row['Sources']
		spp = row['SpeciesCode']

		lw = LengthWeights.objects.get_or_create(
			ModelSpecies = modelSp,
			Sources = source,
			ParameterA = parA,
			ParameterB = parB,
			fbMaxLen = fb_maxL,
			fbMaxLenType = fb_Ltype,
			fbMaxref = fb_maxRef,
			Notes = notes,
			DateUpdated = date,
			SpeciesCode = spp,
			LengthToMeas = LtoMeas,
			Locale = locale,
			fmp_LWid = fmp_LWid
		)
		lw.save()

filename = 'csv_data/Taxonomies.csv'
with open(filename, 'rb') as csvfile:
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

	# FK lookups:
		guild = FunctionalGroups.objects.get_or_create(fmp_guildID=fmp_guild)
		lw = LengthWeights.objects.get_or_create(fmp_LWid=fmp_lw)

	# assigning values:
		spp = Species.objects.get_or_create(
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
			fmp_pk=fmp_speciesID
		)

		spp.save()

filename = 'csv_data/Sites.csv'
with open(filename, 'rb') as csvfile:
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

		sts = Sites.objects.get_or_create(
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

		sts.save()

filename = 'csv_data/Locations.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		name = row['ContainerName']
		ctype = row['ContainerType']
		inst = row['Institution']
		fmp_locationID = row['pk_Location']

		loc = Locations.objects.get_or_create(
			ContainerType = ctype,
			ContainerName = name,
			Institution = inst,
			fmp_locationID = fmp_locationID
		)
		loc.save()

filename = 'csv_data/HHS.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		date = row['DateSurveyed']
		name = row['Names']
		fmp_hhsID = row['pk_hhsID']
		fishing = row['TypicalFishingLocation']
		village = row['Village']

		hhs = HHS.objects.get_or_create(
			Names = name,
			Village = village,
			FishingLocation = fishing,
			DateSurveyed = date
		)
		hhs.save()

filename = 'csv_data/SampleTypes.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		pk_SampleTypeID = row['pk_SampleTypeID']
		stype = row['SampleType']
		TypeCode = row['TypeCode']

		st = SampleTypes.objects.get_or_create(
			SampleType=stype,
			TypeCode=TypeCode,
			fmp_pk=pk_SampleTypeID
		)

		st.save()

filename = 'csv_data/Treatments'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		treat = row['Treatment']
		code = row['TreatmentCode']

		treat = Treatments.objects.get_or_create(
			Treatment=treat,
			TreatmentCode=code
		)

		treat.save()

filename = 'csv_data/Trays.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		tray = row['TrayName']

		tr = Trays.objects.get_or_create(
			TrayName=tray
		)

		tr.save()

filename = 'csv_data/Species_Habitat_Joins.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		fk_FishingHabitat = row['fk_FishingHabitatID']
		fk_SpeciesID = row['fk_SpeciesID']

	# FK lookups:
		hab = FishingHabitats.objects.get_or_create(Habitat=fk_FishingHabitat)
		spp = Species.objects.get_or_create(fmp_pk=fk_SpeciesID)

	# assigning values:
		sh = SpeciesHabitats.objects.get_or_create(
			fk_Habitat=hab,
			fk_Species=spp
		)

		sh.save()

filename = 'csv_data/Species_Method_Join.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		fk_FishingMethodID = row['fk_FishingMethodID']
		fk_SpeciesID = row['fk_SpeciesID']

	# FK lookups:
		meth = FishingMethods.objects.get_or_create(Method=fk_FishingMethodID)
		spp = Species.objects.get_or_create(fmp_pk=fk_SpeciesID)

	# assigning values:
		sm = SpeciesMethods.objects.get_or_create(
			fk_Species=spp,
			fk_Method=meth
		)

		sm.save()



filename = 'csv_data/Specimens.csv'
with open(filename, 'rb') as csvfile:
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
		spe = Specimens.objects.get_or_create(
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

		spe.save()


filename = 'csv_data/Dissections.csv'
with open(filename, 'rb') as csvfile:
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
		obj = Dissections.objects.get_or_create(
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
		obj.save()


filename = 'csv_data/Samples.csv'
with open(filename, 'rb') as csvfile:
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
		samp = Samples.objects.get_or_create(
			fk_Specimen=specimen,
			fk_SampleType=stype,
			SampleID=SampleID,
			Notes=notes,
			fmp_pk=fmp_pk_samp
		)

		samp.save()


filename = 'csv_data/SharkStates.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		State = row['State']

		s = SharkStates.objects.get_or_create(
			State=State
		)

		s.save()

filename = 'csv_data/SharkPieces.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		piece = row['SharkPiece']

	sps = SharkPieces.objects.get_or_create(
		SharkPiece=piece
	)

	sps.save()

filename = 'csv_data/SharkDissections.csv'
with open(filename, 'rb') as csvfile:
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

		sds = SharkDissections.objects.get_or_create(
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

		sds.save()


filename = 'csv_data/SharkSamples.csv'
with open(filename, 'rb') as csvfile:
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

		ss = SharkSamples.objects.get_or_create(
			fk_Sample=samp,
			fk_SharkPiece=piece,
			fk_State=state,
			fk_HHS=hhs
		)

		ss.save()


filename = 'csv_data/Preprocessings.csv'
with open(filename, 'rb') as csvfile:
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
		prep = Preprocessings.objects.get_or_create(
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

		prep.save()

filename = 'csv_data/PackedSamples.csv'
with open(filename, 'rb') as csvfile:
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
		ps = PackedSamples.objects.get_or_create(
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

		ps.save()


filename = 'csv_data/Results.csv'
with open(filename, 'rb') as csvfile:
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
		results = Results.objects.get_or_create(
			fk_Packed=packed,
			d13C=d13C,
			d15N=d15N,
			Lab=Lab,
			DateProcessed=DateProcessed
		)		


filename = 'csv_data/SampleLocations.csv'
with open(filename, 'rb') as csvfile:
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
		sl = SampleLocations.objets.get_or_create(
			fk_Sample=sample,
			fk_Location=loc,
			DateUpdated=DateStatus,
			EnteredBy=EnteredBy,
			Institution=inst
		)

		sl.save()

filename = 'csv_data/SpecimenSpareSamples.csv'
with open(filename, 'rb') as csvfile:
	csvreader = csv.DictReader(csvfile)
	for row in csvreader:
		cont = row['Container']
		inst = row['Institution']
		specimenID = row['ref_SpecimenID']

	# FK lookups:
		spec = Specimens.objects.get_or_create(SpecimenID=specimenID)

	# assigning values:
		sss = SpecimenSpareSamples.objects.get_or_create(
			fk_Specimen=spec,
			Container=cont,
			Institution=inst,
		)

		sss.save()


"""


		






































































