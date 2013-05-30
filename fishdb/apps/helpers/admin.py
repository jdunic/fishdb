from django.contrib import admin
from apps.helpers.models import *
from fishdb.helper import export_model_as_csv


class CMadmin(admin.ModelAdmin):
    list_display = ('Method',)


class HHSadmin(admin.ModelAdmin):
    list_display = ('Names', 'Village', 'FishingLocation', 'DateSurveyed',)


class Ladmin(admin.ModelAdmin):
    list_display = ('ContainerType', 'ContainerName', 'Institution',)


class STadmin(admin.ModelAdmin):
    list_display = ('SampleType', 'TypeCode',)


class SITESadmin(admin.ModelAdmin):
    list_display = ('SiteName', 'ProdFish', 'IslandArea', 'Notes', )


class TRAYadmin(admin.ModelAdmin):
    list_display = ('TrayName', 'Submitted', 'Notes', 'id',)


class TREadmin(admin.ModelAdmin):
    list_display = ('Treatment', 'TreatmentCode',)


class WPadmin(admin.ModelAdmin):
    list_display = ('Waypoint', 'Latitude', 'Longitude', 'Notes', 
        'Year', 'SiteNum', 'id',)



admin.site.register(CollectionMethods, CMadmin)
admin.site.register(HHS, HHSadmin)
admin.site.register(Locations, Ladmin)
admin.site.register(MegaPhotoQuads)
admin.site.register(SampleTypes, STadmin)
admin.site.register(Sites, SITESadmin)
admin.site.register(Trays, TRAYadmin)
admin.site.register(Treatments, TREadmin)
admin.site.register(Waypoints, WPadmin)
































