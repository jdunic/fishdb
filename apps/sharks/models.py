from django.db import models

from apps.data.models import Specimens, \
    Samples
from apps.helpers.models import HHS


class SharkPieces(models.Model):
    SharkPiece = models.CharField(max_length=255, unique=True) 
    # location (e.g., dorsal fin, pectoral fin, dorsal muscle plug) 
    # from which a sample was taken

    def __unicode__(self):
        return u'%s' % (self.SharkPiece)


class SharkStates(models.Model): # type of treatment: e.g., Fresh, sun-dried, 
    # oven-dried (experimental)
    State = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return u'%s' % (self.State)


class SharkHhsJoins(models.Model): # This table allows sharks collected from
    # household surveys to be paired with the appropriate hhs data. 
    fk_SpecimenID = models.ForeignKey(Specimens)
    fk_HHS = models.ForeignKey(HHS, null=True, blank=True)

    def __unicode__(self):
        return u'shark specimen: %s' % (self.fk_SpecimenID.SpecimenID)


class SharkDissections(models.Model): # may need to change fields in this table
# to allow: null=True, blank=True
    fk_Specimen = models.ForeignKey(Specimens, unique=True)
    
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


class SharkSamples(models.Model):
    fk_Sample = models.ForeignKey(Samples)
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
























