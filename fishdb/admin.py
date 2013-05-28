from django.contrib import admin
from fishdb.models import *
from fishdb.helper import export_model_as_csv


# HELPER TABLE Admins: 
# Collection methods, functional groups, fishing habitats, fishing methods, 
#    length-weight, sample locations, household surveys, sites, species, 
#    species types, sample types, treatments, trays
class CMadmin(admin.ModelAdmin):
	list_display = ('Method',)


class FGadmin(admin.ModelAdmin):
    list_display = ('GuildName', 'GuildCode', 'id',)


class FHadmin(admin.ModelAdmin):
	list_display = ('Habitat',)


class FMadmin(admin.ModelAdmin):
	list_display = ('Method', 'id',)


class LWadmin(admin.ModelAdmin):
	list_display = ('SpeciesCode', 'LengthToMeas', 'ParameterA', 'ParameterB',
		'ModelSpecies', 'fbMaxLen', 'fbMaxLenType', 'fbMaxRef', 'Locale', 'Sources',
		'Notes', 'DateUpdated', 'id',)


class Ladmin(admin.ModelAdmin):
    list_display = ('ContainerType', 'ContainerName', 'Institution',)


class HHSadmin(admin.ModelAdmin):
    list_display = ('Names', 'Village', 'FishingLocation', 'DateSurveyed',)



class SITESadmin(admin.ModelAdmin):
    list_display = ('SiteName', 'ProdFish', 'IslandArea', 'Notes', )


class SPadmin(admin.ModelAdmin):
    def get_guild_code(self, o):
        return '%s' % o.fk_Guild.GuildCode
    get_guild_code.short_description = "Guild Code"

    def get_type(self, o):
        return '%s' % o.fk_Type.Type
    get_type.short_description = "Type"

    def habitat_names(self, o):
        return ', '.join(o.Habitats.all().values_list('Habitat', flat=True))
        #return ', '.join([hb.Habitat for hb in o.Habitats.all()])
    #habitat_names.short_description = "Fishing Habitats"

    def method_names(self, o):
        return ', '.join(o.Methods.all().values_list('Method', flat=True))

    list_display = ('SpeciesCode', 'get_guild_code', 'ScientificName', 'Order', 'Family', 'Genus', 'LocalName', 'EnglishName','get_type', 'habitat_names', 'method_names',)

    list_filter = ['fk_Guild__GuildCode']

    search_fields = ['SpeciesCode', 'ScientificName', 'EnglishName']


class SPTYPEadmin(admin.ModelAdmin):
    list_display = ('Type',)


class STadmin(admin.ModelAdmin):
    list_display = ('SampleType', 'TypeCode',)


class TREadmin(admin.ModelAdmin):
    list_display = ('Treatment', 'TreatmentCode',)


class TRAYadmin(admin.ModelAdmin):
    list_display = ('TrayName', 'id')


class WPadmin(admin.ModelAdmin):
    list_display = ('Waypoint', 'Latitude', 'Longitude', 'Notes', 
        'Year', 'SiteNum', 'id',)



# SHARK TABLE Admins - shark helper tables and joins:
# Shark pieces, dissections, samples, specimens, states (experimental) 

class PIECEadmin(admin.ModelAdmin):
    list_display = ('SharkPiece',)


class SHDISadmin(admin.ModelAdmin):
    def get_spec(self, o):
        return '%s' % o.fk_Specimen.SpecimenID
    get_spec.short_description = "SpecimenID"

    list_display = ('get_spec', 'DateDissected', 'PCL', 'FL', 'TL', 'stretch', 
        'DH', 'DB', 'PH', 'PB', 'TH', 'TB', 'wt', 'Notes', )


class SHSAMPadmin(admin.ModelAdmin):
    def get_samp(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_samp.short_description = "SampleID"

    def get_piece(self, o):
        return '%s' % o.fk_SharkPiece.SharkPiece
    get_piece.short_description = "Piece"

    def get_state(self, o):
        return '%s' % o.fk_State.State
    get_state.short_description = "Experimental Treatment"

    list_display = ('get_samp', 'get_piece', 'get_state',)


class SHSPECadmin(admin.ModelAdmin):
    def get_shark_spec(self, o):
        return '%s' % o.fk_SpecimenID.SpecimenID
    get_shark_spec.short_description = "SpecimenID"

    def get_HHS(self, o):
        return '%s %s' % (o.fk_HHS.Names, o.fk_HHS.DateSurveyed)
    get_HHS.short_description = "HHS info"

    list_display = ('get_shark_spec', 'get_HHS',)


class STATEadmin(admin.ModelAdmin):
    list_display = ('State',)  





# DATA TABLE Admins:
# Specimens, dissections, samples, preprocessings, packed samples, results
class SPECadmin(admin.ModelAdmin):
    def get_site_name(self, o):
        return '%s' % o.fk_Site.SiteName
    get_site_name.short_description = "Site"

    def get_species(self, o):
        return '%s' % o.fk_Species.ScientificName
    get_species.short_description = "Species"

    list_display = ('SpecimenID', 'get_species', 'get_site_name', 
        'DepthCollected', 'DateCollected', 'OldID1', 'CollectionNotes', 'id',)

    list_filter = ['fk_Site__SiteName','fk_Species__Genus']

    search_fields = ['SpecimenID']


class DISadmin(admin.ModelAdmin):
    def get_specID(self, o):
        return '%s' % o.fk_Specimen.SpecimenID
    get_specID.short_description = "SpecimenID"
    get_specID.admin_order_field = "fk_Specimen__SpecimenID"
    def get_species(self, o):
        return '%s' % o.fk_Specimen.fk_Species.SpeciesCode
    get_species.short_description = "Species"
    get_species.admin_order_field = "fk_Specimen__fk_Species__SpeciesCode"

    list_display = ('get_specID', 'get_species', 'SizeClass', 'wt', 'SL', 'TL', 
        'FL', 'gh', 'gw', 'PreySize', 'StomachSample', 'StomachContents', 
        'Notes','DissectedBy',)


class SAMPadmin(admin.ModelAdmin):
    def get_specID(self, o):
        return '%s' % o.fk_Specimen.SpecimenID
    get_specID.short_description = "SpecimenID"
    
    def get_species(self, o):
        return '%s' % o.fk_Specimen.fk_Species.SpeciesCode
    get_species.short_description = "Species"

    def get_treat(self, o):
        return '%s' % o.preprocessings_set.get().fk_Treatment.TreatmentCode
    get_treat.short_description = "Treatment"
    get_treat.admin_order_field = 'preprocessings__fk_Treatment__TreatmentCode'

    def get_type(self, o):
        return '%s' % o.fk_SampleType.SampleType
    get_type.short_description = "Sample type"

    list_display = ('SampleID', 'get_specID', 'get_species', 'get_treat', 
        'get_type', 'OldSampleID', 'Notes',)

    list_filter = ['fk_Specimen__fk_Species__Genus', 
                   'preprocessings__fk_Treatment__TreatmentCode']

    search_fields = ['SampleID', 
                     'fk_SampleType__SampleType',
                     'fk_Specimen__fk_Species__SpeciesCode',
                     'preprocessings__fk_Treatment__TreatmentCode']
    actions = (export_model_as_csv,)


class PREPadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    def get_treat(self, o):
        return '%s' % o.fk_Treatment.TreatmentCode
    get_treat.short_description = "Treatment"

    list_display = ('get_sampID', 'get_treat', 'DateWashDry', 'DateGround', 
        'Notes',)

    search_fields = ['fk_Sample__SampleID']


class PSadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    def get_tray(self, o):
        return '%s' % o.fk_TrayName.TrayName
    get_tray.short_description = "Tray"

    list_display = ('get_sampID', 'get_tray', 'TrayRow', 'TrayColumn', 'Notes', 'id', )

    search_fields = ['fk_Sample__SampleID','fk_TrayName__TrayName']


class REadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Packed.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    def get_tray(self, o):
        return '%s' % o.fk_Packed.fk_TrayName.TrayName
    get_tray.short_description = "Tray"

    list_display = ('get_sampID', 'get_tray', 'd13C', 'd15N', 'Lab',)



# Tables: alphabetical order
admin.site.register(CollectionMethods, CMadmin)
admin.site.register(Dissections, DISadmin)
admin.site.register(FishingHabitats, FHadmin)
admin.site.register(FishingMethods, FMadmin)
admin.site.register(FunctionalGroups, FGadmin)
admin.site.register(HHS, HHSadmin)
admin.site.register(LengthWeights, LWadmin)
admin.site.register(Locations, Ladmin)
admin.site.register(MegaPhotoQuads)
admin.site.register(PackedSamples, PSadmin)
admin.site.register(Preprocessings, PREPadmin)
admin.site.register(Results, REadmin)
admin.site.register(SampleLocations)
admin.site.register(Samples, SAMPadmin)
admin.site.register(SampleTypes, STadmin)
admin.site.register(SharkDissections, SHDISadmin)
admin.site.register(SharkPieces, PIECEadmin)
admin.site.register(SharkSamples, SHSAMPadmin)
admin.site.register(SharkSpecimens, SHSPECadmin)
admin.site.register(SharkStates, STATEadmin)
admin.site.register(Sites, SITESadmin)
admin.site.register(Species, SPadmin)
admin.site.register(SpeciesTypes, SPTYPEadmin)
admin.site.register(Specimens, SPECadmin)
admin.site.register(SpecimenSpareSamples)
admin.site.register(Trays, TRAYadmin)
admin.site.register(Treatments, TREadmin)
admin.site.register(Waypoints, WPadmin)
