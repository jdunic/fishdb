from django.db import models

# @TODO: Jillian to complete

class Sites(models.Model):
    Latitude = models.CharField(max_length=255)
    Longitude = models.CharField(max_length=255)
    ocProduct = models.CharField(max_length=255)
    Notes = models.TextField()
    LevelFishing = models.CharField(max_length=255, verbose_name="RTCW 6")
    Region = models.CharField(max_length=255, verbose_name="SWU Region")
    FishingPressure = models.CharField(max_length=255, verbose_name="SWU Fishing pressure")
    BoatAccessibility = models.CharField(max_length=255)
    ShoreEntry = models.CharField(max_length=255)
    IslandArea = models.CharField(max_length=255)
    Productivity = models.CharField(max_length=255,verbose_name="SWU")
    FishingLevel = models.CharField(max_length=255)
    TransitTime = models.CharField(max_length=255)
    fk_WaypointID = models.ForeignKey(Waypoints)
    SiteName = models.CharField(max_length=255)

class Specimens(models.Model):
    fk_SiteID = models.ForeignKey(Sites)
    fk_SpeciesID = models.ForeignKey(Species)
    fk_CollectionMethodID = models.ForeignKey(CollectionMethods)

    SpecimenID = models.CharField(max_length=255, verbose_name="physical label")
    CollectedBy = models.CharField(max_length=255)
    Sex = models.CharField(max_length=255)
    OldID1 = models.CharField(max_length=255, verbose_name="old id 1 ???")
    DateEntered = models.DateTimeField(auto_now_add=True)
    CollectionNotes = models.TextField()
    DateCollected = models.DateField(null=True, blank=True)
    DepthCollected = models.CharField(max_length=255)
    
