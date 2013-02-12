from django.contrib import admin
from fishdb.models import *

class CMadmin(admin.ModelAdmin):
	list_display = ('Method',)

class FHadmin(admin.ModelAdmin):
	list_display = ('Habitat',)

class FMadmin(admin.ModelAdmin):
	list_display = ('Method', 'id',)

class WPadmin(admin.ModelAdmin):
	list_display = ('Waypoint', 'Latitude', 'Longitude', 'Notes', 
		'Year', 'SiteNum', 'id',)

class FGadmin(admin.ModelAdmin):
	list_display = ('GuildName', 'GuildCode', 'id',)

class LWadmin(admin.ModelAdmin):
	list_display = ('SpeciesCode', 'LengthToMeas', 'ParameterA', 'ParameterB',
		'ModelSpecies', 'fbMaxLen', 'fbMaxLenType', 'fbMaxRef', 'Locale', 'Sources',
		'Notes', 'DateUpdated', 'id',)



admin.site.register(CollectionMethods, CMadmin)
admin.site.register(Dissections)
admin.site.register(FishingHabitats, FHadmin)
admin.site.register(FishingMethods, FMadmin)
admin.site.register(FunctionalGroups, FGadmin)
admin.site.register(HHS)
admin.site.register(LengthWeights, LWadmin)
admin.site.register(Locations)
admin.site.register(MegaPhotoQuads)
admin.site.register(PackedSamples)
admin.site.register(Preprocessings)
admin.site.register(Results)
admin.site.register(SampleLocations)
admin.site.register(Samples)
admin.site.register(SampleTypes)
admin.site.register(SharkDissections)
admin.site.register(SharkPieces)
admin.site.register(SharkSamples)
admin.site.register(SharkStates)
admin.site.register(Sites)
admin.site.register(Species)
#admin.site.register(SpeciesHabitats)
#admin.site.register(SpeciesMethods)
admin.site.register(Specimens)
admin.site.register(SpecimenSpareSamples)
admin.site.register(Trays)
admin.site.register(Treatments)
admin.site.register(Waypoints, WPadmin)
