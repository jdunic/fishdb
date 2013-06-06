from django.db import models

from apps.species.models import Species
from apps.helpers.models import Treatments, \
    Sites, \
    CollectionMethods, \
    Trays, \
    Locations, \
    SampleTypes


class Specimens(models.Model):
    fk_Site = models.ForeignKey(Sites)
    fk_Species = models.ForeignKey(Species, null=False, blank=False)
    fk_Method = models.ForeignKey(CollectionMethods, 
        null=True, blank=True)

    SpecimenID = models.CharField(max_length=255, unique=True,
        verbose_name="SpecimenID")
    CollectedBy = models.CharField(max_length=255, null=True, blank=True)
    Sex = models.CharField(max_length=255, null=True, blank=True)
    OldID1 = models.CharField(max_length=255, null=True, blank=True)
    DateEntered = models.DateTimeField(auto_now_add=True)
    CollectionNotes = models.TextField(null=True, blank=True)
    DateCollected = models.DateField(null=True, blank=True)
    # Where this field was null or blank in the original spreadsheets the year 
    # with the date of January 1st #(e.g., 2010-01-01) was added so that queries
    # can be done on collections by year. This date was selected to be 
    # distinguishable from valid dates where they exist.
    DepthCollected = models.CharField(max_length=255, null=True, blank=True)
    # measured in feet!
    
    # makes specimenID appear as an actual specimenID in drop 
        #down menus and such
    def __unicode__(self): 
        return u'%s' % (self.SpecimenID)


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
        else: 
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


class Samples(models.Model):
    fk_Specimen = models.ForeignKey('Specimens')
    fk_SampleType = models.ForeignKey(SampleTypes)

    OldSampleID = models.CharField(max_length=255, null=True, blank=True)
    # OldSampleID is the likely written label (on the bottle/on the label inside
        # the bottle)
    # OldSampleID names may also be found in the notes if not in this field.
    SampleID = models.CharField(max_length=255, unique=True)
    Notes = models.TextField(verbose_name="sample notes", null=True, blank=True)

    def __unicode__(self):
        return u'%s' % (self.SampleID)
        

class Preprocessings(models.Model):
    fk_Sample = models.ForeignKey('Samples', unique=True)
    fk_Treatment = models.ForeignKey(Treatments)
    
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


class PackedSamples(models.Model):
    fk_Sample = models.ForeignKey('Samples')
    fk_TrayName = models.ForeignKey(Trays)
    
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


class Results(models.Model):
#    fk_SampleID = models.ForeignKey('Samples', unique=True)
    # fk_SampleID necessary? I don't think so because of fk_PackedID
    fk_Packed = models.ForeignKey('PackedSamples', unique=True)

    d13C = models.DecimalField(max_digits=20, decimal_places=10)
    d15N = models.DecimalField(max_digits=20, decimal_places=10)
    Lab = models.CharField(max_length=255)
    DateProcessed = models.DateField(null=True, blank=True)
    # date_processed unnecessary? comment out?
    ReliableResult = models.NullBooleanField()

    def __unicode__(self):
        return u'%s result' % (self.fk_Packed.fk_Sample.SampleID)


class SampleLocations(models.Model):
    fk_Sample = models.ForeignKey(Samples)
    fk_Location = models.ForeignKey(Locations)
    
    DateUpdated = models.DateField(auto_now_add=True)
    EnteredBy = models.CharField(max_length=255)

    # FMP fun fact 3: you need to create an extra calculation field to make
        # composite keys before you can constrain your data to have unique
        # field combinations. Woot redundancy.

    class Meta:
        unique_together = ("fk_Sample", "fk_Location", "DateUpdated")

    def __unicode__(self):
        return u'%s' % (self.fk_Location)


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