from django.contrib import admin
from apps.species.models import *
from fishdb.helper import export_model_as_csv



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

    search_fields = ['SpeciesCode']


class SPadmin(admin.ModelAdmin):
    def get_guild_code(self, o):
        try:
            return '%s' % o.fk_Guild.GuildCode
        except AttributeError:
            return None

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

    list_display = ('SpeciesCode', 'get_guild_code', 'ScientificName', 'Order', 
                    'Family', 'Genus', 'LocalName', 'EnglishName','get_type', 
                    'habitat_names', 'method_names',)

    list_filter = ['fk_Guild__GuildCode']

    search_fields = ['SpeciesCode', 'ScientificName', 'EnglishName']


class SPTYPEadmin(admin.ModelAdmin):
    list_display = ('Type',)




admin.site.register(FishingHabitats, FHadmin)
admin.site.register(FishingMethods, FMadmin)
admin.site.register(FunctionalGroups, FGadmin)
admin.site.register(LengthWeights, LWadmin)
admin.site.register(Species, SPadmin)
admin.site.register(SpeciesTypes, SPTYPEadmin)










































