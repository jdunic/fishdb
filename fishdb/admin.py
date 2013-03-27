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

class SPadmin(admin.ModelAdmin):
    def get_guild_code(self, o):
        return '%s' % o.fk_Guild.GuildCode
    get_guild_code.short_description = "Guild Code"

    list_display = ('SpeciesCode', 'get_guild_code', 'ScientificName', 'Order', 'Family', 'Genus', 'LocalName', 'EnglishName',)

    list_filter = ['fk_Guild__GuildCode']

class SITESadmin(admin.ModelAdmin):
    list_display = ('SiteName', 'ProdFish', 'IslandArea', 'Notes', )

class Ladmin(admin.ModelAdmin):
    list_display = ('ContainerType', 'ContainerName', 'Institution',)

class HHSadmin(admin.ModelAdmin):
    list_display = ('Names', 'Village', 'FishingLocation', 'DateSurveyed',)

class STadmin(admin.ModelAdmin):
    list_display = ('SampleType', 'TypeCode',)

class TREadmin(admin.ModelAdmin):
    list_display = ('Treatment', 'TreatmentCode',)

class TRAYadmin(admin.ModelAdmin):
    list_display = ('TrayName',)

class SPECadmin(admin.ModelAdmin):
    def get_site_name(self, o):
        return '%s' % o.fk_Site.SiteName
    get_site_name.short_description = "Site"

    def get_species(self, o):
        return '%s' % o.fk_Species.ScientificName
    get_species.short_description = "Species"

    list_display = ('SpecimenID', 'get_species', 'get_site_name','DepthCollected', 'DateCollected', 'OldID1', 'CollectionNotes', 'id',)

    list_filter = ['fk_Site__SiteName','fk_Species__Genus']

class DISadmin(admin.ModelAdmin):
    def get_specID(self, o):
        return '%s' % o.fk_Specimen.SpecimenID
    get_specID.short_description = "SpecimenID"

    list_display = ('get_specID', 'SizeClass', 'wt', 'SL', 'TL', 'FL', 
        'gh', 'gw', 'PreySize', 'StomachContents', 'Notes','DissectedBy',)


admin.site.register(CollectionMethods, CMadmin)
admin.site.register(Dissections, DISadmin)
admin.site.register(FishingHabitats, FHadmin)
admin.site.register(FishingMethods, FMadmin)
admin.site.register(FunctionalGroups, FGadmin)
admin.site.register(HHS, HHSadmin)
admin.site.register(LengthWeights, LWadmin)
admin.site.register(Locations, Ladmin)
admin.site.register(MegaPhotoQuads)
admin.site.register(PackedSamples)
admin.site.register(Preprocessings)
admin.site.register(Results)
admin.site.register(SampleLocations)
admin.site.register(Samples)
admin.site.register(SampleTypes, STadmin)
admin.site.register(SharkDissections)
admin.site.register(SharkPieces)
admin.site.register(SharkSamples)
admin.site.register(SharkStates)
admin.site.register(Sites, SITESadmin)
admin.site.register(Species, SPadmin)
#admin.site.register(SpeciesHabitats)
#admin.site.register(SpeciesMethods)
admin.site.register(Specimens, SPECadmin)
admin.site.register(SpecimenSpareSamples)
admin.site.register(Trays, TRAYadmin)
admin.site.register(Treatments, TREadmin)
admin.site.register(Waypoints, WPadmin)
