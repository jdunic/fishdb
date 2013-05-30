from django.db import models



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





































