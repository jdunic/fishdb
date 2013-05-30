from django.contrib import admin
from apps.sharks.models import *
from fishdb.helper import export_model_as_csv


class PIECEadmin(admin.ModelAdmin):
    list_display = ('SharkPiece',)


class STATEadmin(admin.ModelAdmin):
    list_display = ('State',)  


class SHSPECadmin(admin.ModelAdmin):
    def get_shark_spec(self, o):
        return '%s' % o.fk_SpecimenID.SpecimenID
    get_shark_spec.short_description = "SpecimenID"

    def get_HHS(self, o):
        return '%s %s' % (o.fk_HHS.Names, o.fk_HHS.DateSurveyed)
    get_HHS.short_description = "HHS info"

    list_display = ('get_shark_spec', 'get_HHS',)


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



admin.site.register(SharkPieces, PIECEadmin)
admin.site.register(SharkStates, STATEadmin)

admin.site.register(SharkSpecimens, SHSPECadmin)
admin.site.register(SharkDissections, SHDISadmin)
admin.site.register(SharkSamples, SHSAMPadmin)

















