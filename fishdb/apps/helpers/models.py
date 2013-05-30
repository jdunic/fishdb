from django.db import models


class CollectionMethods(models.Model):
    Method = models.CharField(max_length=255, unique=True,
        verbose_name="collection method")

    def __unicode__(self):
        return u'%s' % (self.Method)
    # How the samples were collected


class HHS(models.Model): # Household surveys
    Names = models.CharField(max_length=255)
    Village = models.CharField(max_length=255)
    FishingLocation = models.CharField(max_length=255, null=True, blank=True) 
    # typical household fishing location
    DateSurveyed = models.DateField()

    def __unicode__(self):
        return u'%s %s' % (self.Names, self.DateSurveyed)

    fmp_pk = models.IntegerField() # FMP is shit.

    class Meta: 
        unique_together = ("Names", "Village", "DateSurveyed")


class Locations(models.Model): # The box number and type of container (e.g., 
    # scintillation, microtubes) that the DRIED and usually ground sample can
    # be found. This is mostly for samples pre-2012, but in the future this
    # would be handy to have for all samples
    ContainerType = models.CharField(max_length=255)
    ContainerName = models.CharField(max_length=255)
    Institution = models.CharField(max_length=255)
    fmp_locationID = models.IntegerField(null=True, blank=True) # (FMP pk) FMP is shit

    class Meta:
        unique_together = ("ContainerType", "ContainerName", "Institution")

    def __unicode__(self):
        return u'%s %s %s' % (self.ContainerType, 
                              self.ContainerName, 
                              self.Institution
                              )


class MegaPhotoQuads(models.Model):
    fk_Site = models.ForeignKey('Sites')
    fk_Waypoint = models.ForeignKey('Waypoints')
    
    MPQ_Name = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s %s' % (self.MPQ_Name)


class SampleTypes(models.Model):
    SampleType = models.CharField(max_length=255, unique=True) 
    # Sample type, e.g, fish, muscle, POM, algae
    TypeCode = models.CharField(max_length=255, unique=True) 
    # 'code' for sample type

    def __unicode__(self):
        return u'%s' % (self.SampleType)

    fmp_pk = models.IntegerField(null=True, blank=True) # fmp is shit


class Sites(models.Model): #pks are assigned automatically
    SiteName = models.CharField(max_length=255, unique=True)    
    Latitude = models.CharField(max_length=255, null=True, blank=True)
    Longitude = models.CharField(max_length=255, null=True, blank=True)
    IslandArea = models.CharField(max_length=255, null=True, blank=True)
    ProdFish = models.CharField(max_length=255) # Combined productivity and 
        # fishing categories determined by RT and JKB in 2011.
    BoatAccessibility = models.CharField(max_length=255, null=True, blank=True)
    ShoreEntry = models.CharField(max_length=255, null=True, blank=True)
    RTCW_Fishing = models.CharField(max_length=255, 
        verbose_name="RTCW fishing levels", null=True, blank=True) 
        # 6-level fishing pressure catergorisation created by RT and CW in 2010
    FishRank = models.CharField(max_length=255, 
        verbose_name = "fishing level rank (1-6)") # numerically ordered
        # version of the RTCW 6-level fishing categories.
    TransitTime = models.CharField(max_length=255, null=True, blank=True)
    SMWregion = models.CharField(max_length=255, verbose_name="SMW region", 
        null=True, blank=True) # geographic regions used by SMW in PhD thesis
    SMWfishing = models.CharField(max_length=255, null=True, blank=True, 
        verbose_name="SMW fishing pressure") # fishing pressure category based
        # on SMW PhD thesis
    SMWprod = models.CharField(max_length=255, null=True, blank=True,
        verbose_name="SMW productivity") # Productivity category based on SMW
        # PhD thesis
    Notes = models.TextField(verbose_name="site notes", null=True, blank=True)

    #fmp_pk = models.IntegerField(null=True, blank=True) # FMP is shit

    def __unicode__(self):
        return u'%s' % (self.SiteName)


class Trays(models.Model):
    TrayName = models.CharField(max_length=255, unique=True)
    Notes = models.TextField(null=True, blank=True)
    # can include comments about lost samples (none added to here yet),
    # or general comments about the tray such as whether it was renamed,
    # or quality of the results (e.g., RTKI-001 results should not be used)
    Submitted = models.BooleanField()

    def __unicode__(self):
        return u'%s' % (self.TrayName)


class Treatments(models.Model):
    Treatment = models.CharField(max_length=255, unique=True) 
    # raw, acidified, non-acidified, no treatment
    TreatmentCode = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.TreatmentCode)


class Waypoints(models.Model):
    Waypoint = models.CharField(max_length=255) # name of waypoint
    Latitude = models.CharField(max_length=255)
    Longitude = models.CharField(max_length=255)
    Notes = models.CharField(max_length=255, verbose_name="waypoint notes",
        null=True, blank=True)
    Year = models.DateField(verbose_name="year ground truthed", 
        null=True, blank=True)
    # For original data where no month or day was given, August 31 was added
    # to the year for completion
    SiteNum = models.CharField(max_length=255, null=True, blank=True,
        verbose_name="site")
    # could have had this "SiteNum" be a fk lookup, but this leaves the 
        # opportunity to store more than just the classified sites that are in 
        # the Sites table.

    class Meta:
        unique_together = ("Waypoint", "Year")

    def __unicode__(self):
        return u'%s' % (self.Waypoint)



























