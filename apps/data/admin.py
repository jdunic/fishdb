from django.contrib import admin
from apps.data.models import *
from fishdb.helper import export_model_as_csv


class SPECadmin(admin.ModelAdmin):
    def get_site_name(self, o):
        return '%s' % o.fk_Site.SiteName
    get_site_name.short_description = "Site"

    def get_species(self, o):
        return '%s' % o.fk_Species.ScientificName
    get_species.short_description = "Species"

    list_display = ('SpecimenID', 'get_species', 'get_site_name', 
        'DepthCollected', 'DateCollected', 'OldID1', 'CollectionNotes', 'id',)

    list_filter = ['fk_Species__fk_Type__Type',
                   'fk_Site__SiteName',
                   'fk_Species__Genus']

    search_fields = ['SpecimenID', 
                     'fk_Species__SpeciesCode']


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

    search_fields = ['fk_Specimen__SpecimenID', 
        'fk_Specimen__fk_Species__SpeciesCode']


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

    def get_packed(self, o):
        return ', '.join(o.packedsamples_set.all().values_list('TrayRow', flat=True))
    get_packed.short_description = "packed"

#return ', '.join(o.Habitats.all().values_list('Habitat', flat=True))

    list_display = ('SampleID', 'get_specID', 'get_species', 'get_treat', 
        'get_type', 'OldSampleID', 'Notes', 'id', 'get_packed',)

    list_filter = ['fk_Specimen__fk_Species__fk_Type__Type', 
                   'preprocessings__fk_Treatment__TreatmentCode'
                   ]

    search_fields = ['SampleID', 
                     'OldSampleID',
                     'fk_SampleType__SampleType',
                     'fk_Specimen__fk_Species__SpeciesCode',
                     'preprocessings__fk_Treatment__TreatmentCode']
    
    actions = (export_model_as_csv,)

class BARadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    list_display = ('get_sampID', 'TrayName', 'DateSubmitted', 'TrayPosition', )
    list_filter = ['fk_Sample__fk_Specimen__fk_Site__SiteName', 
                   'fk_Sample__fk_Specimen__fk_Species__fk_Guild__GuildCode']

class BARRESadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Barcoded.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    list_display = ('get_sampID', 'Species', 'DateProcessed', )
    list_filter = ['fk_Barcoded__fk_Sample__fk_Specimen__fk_Site__SiteName', 
                   'fk_Barcoded__fk_Sample__fk_Specimen__fk_Species__fk_Guild__GuildCode']

class PREPadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    def get_treat(self, o):
        return '%s' % o.fk_Treatment.TreatmentCode
    get_treat.short_description = "Treatment"
    get_treat.admin_order_field = "fk_Treatment__TreatmentCode"

    list_display = ('get_sampID', 'get_treat', 'DateWashDry', 'DateGround', 
        'Notes',)

    search_fields = ['fk_Sample__SampleID',
                     'fk_Sample__fk_Specimen__fk_Species__fk_Type__Type']


class PSadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"

    def get_tray(self, o):
        return '%s' % o.fk_TrayName.TrayName
    get_tray.short_description = "Tray"
    get_tray.admin_order_field = "fk_TrayName__TrayName"

    def get_treat(self, o):
        return '%s' % o.fk_Sample.preprocessings_set.get().fk_Treatment.TreatmentCode
    get_treat.short_description = "Treatment"

    list_display = ('get_sampID', 'get_tray', 'TrayRow', 'TrayColumn', 'Notes',
                    'get_treat', 'id', )

    search_fields = ['fk_Sample__SampleID','fk_TrayName__TrayName']

    list_filter = ['fk_Sample__preprocessings__fk_Treatment__TreatmentCode',
                   'fk_Sample__fk_Specimen__fk_Species__fk_Type__Type']


class REadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Packed.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"
    get_sampID.admin_order_field = "fk_Packed__fk_Sample__SampleID"

    def get_tray(self, o):
        return '%s' % o.fk_Packed.fk_TrayName.TrayName
    get_tray.short_description = "Tray"

    list_display = ('get_sampID', 'get_tray', 'd13C', 'd15N', 'Lab', 
                    'ReliableResult',)

    search_fields = ['fk_Packed__fk_Sample__SampleID',
                     'fk_Packed__fk_TrayName__TrayName',
                     'Lab', 
                     'fk_Packed__fk_Sample__fk_Specimen__fk_Species__SpeciesCode'
                     ]

    list_filter = ['fk_Packed__fk_Sample__fk_Specimen__fk_Species__fk_Type__Type',
                   'ReliableResult']

class SLOCadmin(admin.ModelAdmin):
    def get_sampID(self, o):
        return '%s' % o.fk_Sample.SampleID
    get_sampID.short_description = "SampleID"
    get_sampID.admin_order_field = "fk_Location__fk_Sample__SampleID"

    def get_institution(self, o):
        return '%s' % o.fk_Location.Institution
    get_institution.short_description = "Institution"


    list_display = ('get_sampID', 'Status', 'get_institution', 'ContainerType',
                    'ContainerName')

    search_fields = ['fk_Location__fk_Sample__SampleID',
                     'fk_Location',
                     'Status'
                     ]

    list_filter = ['Status',
                   'fk_Location'
                   ]


admin.site.register(Specimens, SPECadmin)
admin.site.register(Dissections, DISadmin)
admin.site.register(Samples, SAMPadmin)
admin.site.register(BarcodedSamples, BARadmin)
admin.site.register(BarcodedResults, BARRESadmin)
admin.site.register(Preprocessings, PREPadmin)
admin.site.register(PackedSamples, PSadmin)
admin.site.register(Results, REadmin)
admin.site.register(SampleLocations, SLOCadmin)
admin.site.register(SpecimenSpareSamples)






























