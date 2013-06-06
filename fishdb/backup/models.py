###### After import is done search for CHANGE and fix the auto_update_now option)

from django.db import models
import csv


class CollectionMethods(models.Model):
    Method = models.CharField(max_length=255, unique=True,
        verbose_name="collection method")

    def __unicode__(self):
        return u'%s' % (self.Method)
    # How the samples were collected

#    @classmethod
#    def import_csv(cls, filename='csv_data/CollectionMethods.csv'):
#        with open(filename, 'rU') as csvfile:
#            csvreader = csv.DictReader(csvfile)
#            for row in csvreader:
#                method = row['CollectionMethod']
#                print method
#                cm, created = cls.objects.get_or_create(
#                    Method=method
#                )

                # get_or_create returns a tuple of the object created or 
                # retrieved and whether it was created or retrieved.
                # therefore I have to save only the object of the tuple if
                # it was actually created:

 #               if created:
 #                   cm.save()


class Dissections(models.Model):
    fk_Specimen = models.ForeignKey('Specimens', unique=True)
    TL = models.DecimalField(max_digits=20, decimal_places=3, null=True, 
        blank=True, verbose_name="total length (mm)")
    FL = models.DecimalField(max_digits=20, decimal_places=3, null=True, 
        blank=True, verbose_name="fork length (mm)")
    SL = models.DecimalField(max_digits=20, decimal_places=3, null=True, 
        blank=True, verbose_name="standard length (mm)")
    wt = models.DecimalField(max_digits=20, decimal_places=3, null=True, 
        blank=True, verbose_name="weight (g)")
    gh = models.DecimalField(max_digits=20, decimal_places=3, null=True, 
        blank=True, verbose_name="gape height (mm)")
    gw = models.DecimalField(max_digits=20, decimal_places=3, null=True, 
        blank=True, verbose_name="gape width (mm)")

    def SizeClass(self):   # Adding a method to this model to store calculated
    #SizeClasses
        "Log2 size class"
        if self.wt > 0 and self.wt < 0.0625:
            return "<0.0625 g"
        if self.wt > 0.0625 and self.wt <= 0.125:
            return "0.0625 - 0.125 g"
        if self.wt > 0.125 and self.wt <= 0.250:
            return "0.125 - 0.250 g" 
        if self.wt > 0.250 and self.wt <= 0.500:
            return "0.250 - 0.500 g"       
        if self.wt > 0.500 and self.wt <= 1.000:
            return "0.5 - 1 g"        
        if self.wt > 1 and self.wt <= 2:
            return "1 - 2 g"        
        if self.wt > 2 and self.wt <= 4:
            return "2 - 4 g"
        if self.wt > 4 and self.wt <= 8:
            return "4 - 8 g"
        if self.wt > 8 and self.wt <= 16:
            return "8 - 16 g"
        if self.wt > 16 and self.wt <= 32:
            return "16 - 32 g"
        if self.wt > 32 and self.wt <= 64:
            return "32 - 64 g"
        if self.wt > 64 and self.wt <= 128:
            return "64 - 128 g"
        if self.wt > 128 and self.wt <= 256:
            return "128 - 256 g"  
        if self.wt > 256 and self.wt <= 512:
            return "256 - 512 g"  
        if self.wt > 512 and self.wt <= 1024:
            return "512 - 1024 g"  
        if self.wt > 1024 and self.wt <= 2048:
            return "1.02 - 2.05 kg"  
        if self.wt > 2048 and self.wt <= 4096:
            return "2.05 - 4.10 kg"  
        if self.wt > 4096 and self.wt <= 8192:
            return "4.10 - 8.19 kg"
        if self.wt > 8192 and self.wt <= 16384:
            return "8.19 - 16.38 kg"  
        if self.wt > 16384 and self.wt <= 32768:
            return "16.38 - 32.77 kg"  
        if self.wt > 32768 and self.wt <= 65536:
            return "32.77 - 65.54 kg"  
        if self.wt > 65536 and self.wt <= 131072:
            return "65.54 - 131.07 kg"  
        return "No Value" 

    DateDissected = models.DateField(null=True, blank=True)
    DateEntered = models.DateField(auto_now_add=True) ## CHANGE after imports #######
    StomachContents = models.TextField(null=True, blank=True)
    # Also includes some intestinal contents (Clearly noted as Intestines: blah
        # blah blah)
    PreySize = models.TextField(verbose_name="prey size in stomach", 
        null=True, blank=True)
    # Typically given in mm, unless otherwise noted
    #StomachSample = models.CharField(max_length=225, null=True, blank=True)
    StomachSample = models.NullBooleanField() 
    # Null means that it is unknown whether a stomach sample exists. Ideally
    # these can be filled in as the samples are used and accounted for.
    IsotopeSample = models.CharField(max_length=255, null=True, blank=True) 
    # In recent years this is a of samples taken. 
    # However, early data has just Y/N
    OtolithSample = models.TextField(null=True, blank=True) 
    # Otolith redundancy in original FMP tables was removed and all fields \
    # combined into this one. This is a text field because sometimes there are 
    # just notes about the otoliths. 
    GonadsRipe = models.CharField(max_length=255, null=True, blank=True) 
    # Typically y/n or NA also no longer kept track of in recent data 
    # (2011, 2012)
    PhotoName = models.CharField(max_length=255, verbose_name="photo file name",
        null=True, blank=True)
    DissectedBy = models.CharField(max_length=255, null=True, blank=True)
    Notes = models.TextField(verbose_name="dissection notes", 
        null=True, blank=True) # may include parasitological notes

    def __unicode__(self):
        return u'%s dissection' % (self.fk_Specimen.SpecimenID)

# Filemaker pro fun fact 1: importing a table with fk lookups requires the most
    # stupid procedure... including redunant columns... 
    # This should be your first tip off that it is NOT worth using.

class FishingHabitats(models.Model):
    Habitat = models.CharField(max_length=255, unique=True) # Habitat type where 
    # local fishers classify catching fish
    def __unicode__(self):
        return u'%s' % (self.Habitat)


class FishingMethods(models.Model):
    Method = models.CharField(max_length=255, unique=True,
        verbose_name="fishing method") # Method that local fishers
    # typically catch a given fish species.
    def __unicode__(self):
        return u'%s' % (self.Method)

class FunctionalGroups(models.Model):
    GuildName = models.CharField(max_length=255, unique=True) # verbose name
    GuildCode = models.CharField(max_length=255, unique=True) # one or two letter code
    # assigned to functional groups
    fmp_guildID = models.IntegerField() ### FMP is shit 

    def __unicode__(self):
        return u'%s' % (self.GuildCode)

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

class LengthWeights(models.Model): # Length to weight conversion values
# These LW conversions were given to RT by SMW in 2009 and the original data 
# came from Stuart Sandin and Alan Friedlander; RT subsequently added new 
# columns as indicated by the author field in this definitions sheet 
    ModelSpecies = models.CharField(max_length=255, null=True, blank=True) # Found as a species code. 
    # In the future a field that has the actual scientific name might want to 
    # be added as with the codes (not necessarily in our taxonomies table) it is
    # not immediately obvious what species it is.
    Sources = models.CharField(max_length=255, null=True, blank=True) 
    # The abbreviations should be cleaned up so that future people know 
    # where they came from.
    ParameterA = models.DecimalField(max_digits=30, decimal_places=10, 
        verbose_name="parameter a (for cm to g)", null=True, blank=True)
    ParameterB = models.DecimalField(max_digits=30, decimal_places=10,
        verbose_name="parameter b (for cm to g)", null=True, blank=True)
    fbMaxLen = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="FishBase max length (mm)", null=True, blank=True) 
        # species max length, from FishBase collected by RT workstudy students 
        # in 2011 with max length recorded in mm
    fbMaxLenType = models.CharField(max_length=255,
        verbose_name="FishBase max length type", null=True, blank=True)
    fbMaxRef = models.CharField(max_length=255, 
        verbose_name="FishBase reference for max length", null=True, blank=True)
    # Typically the numeric code that FishBase assigns to its references in the
    # references section 
    Notes = models.TextField(null=True, blank=True) #descriptive notes including changes or updates
    DateUpdated = models.DateField(null=True, blank=True) # Date of last change --> Django will
    # automatically update this field when a change is made and save() happens
    #Jillian CHANGE this to auto_now_add once migration complete
    #SpeciesName = models.CharField(max_length=255, 
     #   verbose_name="scientific name", null=True, blank=True)
    # Could use a clean up with current FishBase naming conventions
    SpeciesCode = models.CharField(max_length=255) # RT species codes to index
    # against taxonomies
    # Scientific names have been error prone so we are using SpeciesCodes to 
    # do all of our lookups and for data recording.
    LengthToMeas = models.CharField(max_length=255,
        verbose_name="length to measure", null=True, blank=True)
    # length for which theh parameters are used to calculate/reverse calc
    Locale = models.CharField(max_length=255, null=True, blank=True) 
    # location where LW measurements recorded
    fmp_LWid = models.IntegerField(null=True, blank=True) # FMP is shit

    def __unicode__(self):
        return u'Model Species: %s' % (self.ModelSpecies)

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

##### MPQ's, one source of information on what sites you can find MPQs are in 
    # the Dropbox > stable_isotope_database > input_data >
    # site_classifications.xls file 

class PackedSamples(models.Model):
    fk_Sample = models.ForeignKey('Samples')
    fk_TrayName = models.ForeignKey('Trays')
    
    TrayRow = models.CharField(max_length=1)
    TrayColumn = models.IntegerField()
    CapWeight = models.DecimalField(max_digits=10, decimal_places=4,
        null=True, blank=True)
    FilledCapWeight = models.DecimalField(max_digits=10, decimal_places=4,
        null=True, blank=True)
    SampleWeight = models.DecimalField(max_digits=10, decimal_places=4,
        null=True, blank=True) 
    PackedBy = models.CharField(max_length=255)
    EnteredBy = models.CharField(max_length=255)
    DatePacked = models.DateField(null=True, blank=True)
    DateEntered = models.DateField(auto_now_add=True)
    Notes = models.TextField(verbose_name="packed sample notes", 
        null=True, blank=True)

    fmp_packedID = models.IntegerField(null=True, blank=True) # fmp is shit

    # Filemaker pro fun fact 2: if you want to make sure you export all the data
        # from a single table... make damn well sure you have ALL records 
        # displayed. Otherwise you'll have to export those tables all over again

    class Meta:
        unique_together = ("fk_TrayName", "TrayRow", "TrayColumn")

    def __unicode__(self):
        return u'Sample: %s in %s  %s%s' % (self.fk_Sample.SampleID,
                              self.fk_TrayName.TrayName,
                              self.TrayRow,
                              self.TrayColumn
                              )

class Preprocessings(models.Model):
    fk_Sample = models.ForeignKey('Samples', unique=True)
    fk_Treatment = models.ForeignKey('Treatments')
    
    DateWashDry = models.DateField(null=True, blank=True)
    PreppedBy = models.CharField(max_length=255, null=True, blank=True)
    EnteredBy = models.CharField(max_length=255, null=True, blank=True,
        verbose_name="prep entered by")
    DateGround = models.DateField(null=True, blank=True)
    DryingMethod = models.CharField(max_length=255)
    DryingTime = models.CharField(max_length=255, null=True, blank=True)
    Notes = models.TextField(verbose_name="preprocessing notes",
        null=True, blank=True)

    def __unicode__(self):
        return u'%s treatment: %s' % (self.fk_Sample.SampleID,
                                      self.fk_Treatment.TreatmentCode
                                      )

    #fmp_preprocessings = models.IntegerField(null=True, blank=True) # fmp is shit

class Results(models.Model):
#    fk_SampleID = models.ForeignKey('Samples', unique=True)
    # fk_SampleID necessary? I don't think so because of fk_PackedID
    fk_Packed = models.ForeignKey('PackedSamples', unique=True)

    d13C = models.DecimalField(max_digits=20, decimal_places=10)
    d15N = models.DecimalField(max_digits=20, decimal_places=10)
    Lab = models.CharField(max_length=255)
    DateProcessed = models.DateField(null=True, blank=True)
    # date_processed unnecessary? comment out?
    def __unicode__(self):
        return u'%s result' % (self.fk_Packed.fk_Sample.SampleID)


class SampleLocations(models.Model):
    fk_Sample = models.ForeignKey('Samples')
    fk_Location = models.ForeignKey('Locations')
    
    DateUpdated = models.DateField(auto_now_add=True)
    EnteredBy = models.CharField(max_length=255)

    # FMP fun fact 3: you need to create an extra calculation field to make
        # composite keys before you can constrain your data to have unique
        # field combinations. Woot redundancy.

    class Meta:
        unique_together = ("fk_Sample", "fk_Location", "DateUpdated")

    def __unicode__(self):
        return u'%s' % (self.fk_Location)

class Samples(models.Model):
    fk_Specimen = models.ForeignKey('Specimens')
    fk_SampleType = models.ForeignKey('SampleTypes')

    OldSampleID = models.CharField(max_length=255, null=True, blank=True)
    # OldSampleID is the likely written label (on the bottle/on the label inside
        # the bottle)
    # OldSampleID names may also be found in the notes if not in this field.
    SampleID = models.CharField(max_length=255, unique=True)
    Notes = models.TextField(verbose_name="sample notes", null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.SampleID)

    # FMP fun fact 4: on average, it takes a user 6 months of using FMP before
        # they break and move to a real db solution.


class SampleTypes(models.Model):
    SampleType = models.CharField(max_length=255, unique=True) 
    # Sample type, e.g, fish, muscle, POM, algae
    TypeCode = models.CharField(max_length=255, unique=True) 
    # 'code' for sample type

    def __unicode__(self):
        return u'%s' % (self.SampleType)

    fmp_pk = models.IntegerField(null=True, blank=True) # fmp is shit

class SharkDissections(models.Model): # may need to change fields in this table
# to allow: null=True, blank=True
    fk_Specimen = models.ForeignKey('Specimens', unique=True)
    
    PCL = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="precaudal length (cm)")
    FL = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="fork length (cm)")
    TL = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="total length (cm)")
    stretch = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="stretch length (cm)")
    DH = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="dorsal fin height (cm)")
    DB = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="dorsal fin base length (cm)")
    PH = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="pectoral fin height (cm)")
    PB = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="pectoral fin base length (cm)")
    TH = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="tail height (cm)")
    TB = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="tail base length (cm)")
    wt = models.DecimalField(max_digits=20, decimal_places=3,
        verbose_name="weight (lbs)")
    PhotoTaken = models.CharField(max_length=255) # so far this has just been
    # Y/N
    Notes = models.TextField(verbose_name="shark dissection notes")
    DateDissected = models.DateField()

    def __unicode__(self):
        return u'shark: %s dissection' % (self.fk_Specimen.SpecimenID)

class SharkPieces(models.Model):
    SharkPiece = models.CharField(max_length=255, unique=True) 
    # location (e.g., dorsal fin, pectoral fin, dorsal muscle plug) 
    # from which a sample was taken

    def __unicode__(self):
        return u'%s' % (self.SharkPiece)

class SharkSamples(models.Model):
    fk_Sample = models.ForeignKey('Samples')
    fk_SharkPiece = models.ForeignKey('SharkPieces')
    fk_State = models.ForeignKey('SharkStates')
#    fk_HHS = models.ForeignKey('HHS', null=True, blank=True)
#    FromHHS = models.BooleanField() # Is the shark sample from a HHS? 
    # A true/false field.
    
    DateDissected = models.DateField() # Date that a shark piece was dissected
    # into bits like muscle, skin, ray, etc.
    #Notes = models.TextField(verbose_name="shark sample notes", 
     #   null=True, blank=True)

    def __unicode__(self):
        return u'shark sample: %s' % (self.fk_Sample.SampleID)

class SharkHhsJoins(models.Model): # This table allows sharks collected from
    # household surveys to be paired with the appropriate hhs data. 
    fk_SpecimenID = models.ForeignKey('Specimens')
    fk_HHS = models.ForeignKey('HHS', null=True, blank=True)

    def __unicode__(self):
        return u'shark specimen: %s' % (self.fk_SpecimenID.SpecimenID)

class SharkStates(models.Model): # type of treatment: e.g., Fresh, sun-dried, 
    # oven-dried (experimental)
    State = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.State)


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

class Species(models.Model): # Taxonomic information
    ScientificName = models.CharField(max_length=255, null=True, blank=True)
    Order = models.CharField(max_length=255, null=True, blank=True)
    Family = models.CharField(max_length=255, null=True, blank=True)
    Genus = models.CharField(max_length=255, null=True, blank=True)
    LocalName = models.CharField(max_length=255, null=True, blank=True)
    EnglishName = models.CharField(max_length=255, null=True, blank=True)
    SpeciesCode = models.CharField(max_length=255, unique=True, 
        null=True, blank=True)
    Notes = models.TextField(verbose_name="taxonomic notes", 
        null=True, blank=True)

    fk_Guild = models.ForeignKey('FunctionalGroups', null=True, blank=True)
    fk_LengthWeight = models.ForeignKey('LengthWeights', null=True, blank=True)
    fk_Type = models.ForeignKey('SpeciesTypes')
    # species types: fish, macro, shark, urchin, turtle, lobster, worm

###### ADD Many-to-Many??????
    Habitats = models.ManyToManyField('FishingHabitats')
    Methods = models.ManyToManyField('FishingMethods')

    def habitat_names(self):
        return ', '.join([a.Habitats for a in self.FishingHabitats.all()])

    def __unicode__(self):
        return u'%s' % (self.SpeciesCode)

    # to be deleted!
    fmp_pk = models.IntegerField(null=True, blank=True)

class SpeciesTypes(models.Model): # urchin, shark, macro, fish
    Type = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s' % (self.Type)


class Specimens(models.Model):
    fk_Site = models.ForeignKey('Sites')
    fk_Species = models.ForeignKey('Species', null=False, blank=False)
    fk_Method = models.ForeignKey('CollectionMethods', 
        null=True, blank=True)

    SpecimenID = models.CharField(max_length=255, unique=True,
        verbose_name="SpecimenID")
    CollectedBy = models.CharField(max_length=255, null=True, blank=True)
    Sex = models.CharField(max_length=255, null=True, blank=True)
    OldID1 = models.CharField(max_length=255, null=True, blank=True)
    DateEntered = models.DateTimeField(auto_now_add=True)
    CollectionNotes = models.TextField(null=True, blank=True)
    DateCollected = models.DateField(null=True, blank=True)
    DepthCollected = models.CharField(max_length=255, null=True, blank=True)
    # measured in feet!
    
    # makes specimenID appear as an actual specimenID in drop 
        #down menus and such
    def __unicode__(self): 
        return u'%s' % (self.SpecimenID)
# Note: a count query of specimens will produce a higher number of specimens
# than actually sampled. Shark specimens do not always represent individuals. 
# There are single sharks represented by multiple specimenIDs



class SpecimenSpareSamples(models.Model):
    fk_Specimen = models.ForeignKey('Specimens')
    Container = models.CharField(max_length=255, null=True, blank=True,
        verbose_name="archived sample container name")
    Institution = models.CharField(max_length=255)
    DateUpdated = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'%s spare location: %s' % (self.fk_Specimen.SpecimenID,
                                           self.Container
                                           )

#    class Meta:
#        unique_together = ("fk_Specimen", "DateUpdated")
# Not sure if this method is necessary... we're not doing a good job of keeping
    # track of where samples even are...

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
    # raw, acidified, non-acidified
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





















