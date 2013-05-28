#!/usr/bin/env python
"""
git add -A
then type
git commit -m "updates"
then type
git push
"""

"""
source venv/bin/activate
"""

# setup django
import os
import csv
import collections
from datetime import datetime
from decimal import Decimal
import logging
import sys
from subprocess import call

from django.core.management import setup_environ
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist, ValidationError


from fishdb import settings
from fishdb.models import *

setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")

logging.basicConfig(level=logging.INFO)

def shitty_date_conversion(dt_str, blank=False):
    dt = None

    try:
        dt = datetime.strptime(dt_str, "%d-%b-%y")
    except:
        try:
            dt = datetime.strptime(dt_str, "%d.%m.%Y")
        except:
            try:
                dt = datetime.strptime(dt_str, "%d.%m.%y")    
            except:
                try:
                    dt = datetime.strptime(dt_str, "%Y-%m-%d")
                except:
                    try:
                        dt = datetime.strptime(dt_str, "%b-%d-%Y")
                    except:
                        try:
                            dt = datetime.strptime(dt_str, "%d-%m-%Y")
                        except:
                            pass

    if not dt and not blank:
        raise Exception('%s is a shitty date' % dt_str)
    return dt


def cm_import():
    filename = 'csv_data/CollectionMethods.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            method = row['CollectionMethod']
            #print method
            cm, created = CollectionMethods.objects.get_or_create(
                Method=method
            )
            # "cm, created" tells django to put the object first, then boolean 
            # for created in that order: (obj, T/F) 
            # get_or_create returns a tuple of the object created or 
            # retrieved and whether it was created or retrieved.
            # therefore I have to save only the object of the tuple if
            # it was actually created:

            if created:
                #cm.Method=method  # not necessary because we already 
                # told it Method=method in the 'cm, created = ...'
                cm.save()
        
def fh_import():
    filename = 'csv_data/FishingHabitats.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            habitat = row['FishingHabitat']

            habs, created = FishingHabitats.objects.get_or_create(
                Habitat = habitat
            )

            if created:
                habs.save()

def fm_import():    
    filename = 'csv_data/FishingMethods.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
                method = row['FishingMethod']

                meths, created = FishingMethods.objects.get_or_create(
                    Method = method
                )

                if created:
                    meths.save()

def wp_import():
    filename = 'csv_data/Waypoints.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            lat = row['Latitude']
            longit = row['Longitude']
            notes = row['Notes']
            SiteNum = row['SiteNo']
            wp = row['Waypoint']
            year = row['YearGroundTruthed']

            yeard = None
            if year != '':
                yeard = datetime.strptime(year, '%Y-%m-%d').date()

            wps, created = Waypoints.objects.get_or_create(
                Waypoint=wp,
                Latitude=lat,
                Longitude=longit,
                Notes=notes,
                Year=yeard,
                SiteNum=SiteNum
            )
            
            if created:
                wps.save()

def fg_import():
    filename = 'csv_data/FunctionalGroups.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            fmp_guildID = row['pk_GuildID']
            code = row['GuildCode']
            guild = row['GuildName']

            g, created = FunctionalGroups.objects.get_or_create(
                GuildName = guild,
                GuildCode = code,
                fmp_guildID = fmp_guildID
            )
            
            if created:
                g.save()

def lw_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/kx_fish_LW_rels.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)

        line_number = 1
        for row in csvreader:
            line_number += 1
            date = row['Date Updated']
            fb_maxL = row['lmax.fishbase.mm']
            fb_maxRef = row['lmax.fishbase.ref']
            fb_Ltype = row['fishbase.lmax.type']
            LtoMeas = row['TypLen']
            locale = row['Locale']
            modelSp = row['ModelSp']
            notes = row['notes']
            parA = row['a (to use, cm)']
            parB = row['b (to use, cm)']
            source = row['Sources']
            spp = row['sp']

        # Putting date in datetime format:
            dated = datetime.strptime(date, '%Y-%m-%d').date()

        # Putting number strings into decimals (and watching out for NULLS!!!!):
            
            if fb_maxL == '' or fb_maxL == 'NA':
                fb_L = None
            else:
                fb_L = Decimal(fb_maxL)
            
            if parA == '' or parA == 'NA':
                A = None
            else: 
                A = Decimal(parA)
            
            if parB == '' or parB == 'NA':
                B = None
            else:
                B = Decimal(parB)

            lw, created = LengthWeights.objects.get_or_create(
                ModelSpecies = modelSp,
                Sources = source,
                ParameterA = A,
                ParameterB = B,
                fbMaxLen = fb_L,
                fbMaxLenType = fb_Ltype,
                fbMaxRef = fb_maxRef,
                Notes = notes,
                DateUpdated = dated,
                SpeciesCode = spp,
                LengthToMeas = LtoMeas,
                Locale = locale
            )

            if created:
                lw.save()


def sp_type():
    filename='csv_data/SpeciesTypes.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            Type = row['SpeciesType']

            spt = SpeciesTypes.objects.create(
                Type=Type) 

def sp_import(filename = 'csv_data/Taxonomies.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            EnglishName = row['EnglishName']
            family = row['Family']
            fmp_guild = row['fk_GuildID']
            fmp_lw = row['fk_LengthWeightID']
            LocalName = row['LocalName']
            notes = row['Notes']
            order = row['Order']
            #fmp_speciesID = row['pk_SpeciesID']
            SciName = row['ScientificName']
            code = row['SpeciesCode']
            guild = None
            lw = None
            Type = row['Type']


            # make genus (may as well)
            genus = None
            try:    
                genus = str.split(SciName)[0]
            except:
                pass

            # make shit an int... IF not ''
            #if fmp_speciesID == '':
             #   fmp_pk = None

            #if fmp_speciesID is None:
             #   fmp_pk = None
            #else:
             #   fmp_pk = int(fmp_speciesID)

            if fmp_guild == '':
                guild1 = None
            else:
                guild1 = int(fmp_guild)

            if fmp_lw == '':
                lw1 = None
            else:
                lw1 = int(fmp_lw)
            
            # FK lookups:
            if guild1 is not None:
                guild, created = FunctionalGroups.objects.get_or_create(fmp_guildID=guild1)
                if created:
                    logging.info('created guild: %s' % guild)
                    guild.save()
            if lw1 is not None:
                lw, created = LengthWeights.objects.get_or_create(fmp_LWid=lw1)
                #if created:
                 #   logging.info('created lengthweights: %s' % lw)
                lw.save()

            Type = SpeciesTypes.objects.get(Type=Type)


            try:
                spp = Species.objects.create(
                    ScientificName=SciName,
                    Order=order,
                    Family=family,
                    Genus=genus,
                    LocalName=LocalName,
                    EnglishName=EnglishName,
                    SpeciesCode=code,
                    Notes=notes,
                    fk_Guild=guild,
                    fk_LengthWeight=lw,
                    fk_Type=Type
                )
                spp.save()
            except IntegrityError as e:
                logging.warn("%s:%s Duplicate Species code: %s" % (filename, line_number, code))
            line_number += 1

def sites_import():
    filename = 'csv_data/Sites.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            boat = row['BoatAccessibility']
            ProdFish = row['CombinedFishingProductivity']
            notes = row['DescriptiveNotes']
            FishRank = row['FishingLevel']
            IslandArea = row['IslandArea']
            Latitude = row['Latitude']
            Longitude = row['Longitude']
            fmp_siteID = row['pk_SiteID']
            RTCW_Fishing = row['RTCW_6_LevelFishing']
            ShoreEntry = row['ShoreEntry']
            SiteName = row['SiteName']
            SMWfishing = row['SMW_FishingPressure']
            SMWprod = row['SMW_Productivity']
            SMWregion = row['SMW_Region']
            TransitTime = row['TransitTime']

            sts, created = Sites.objects.get_or_create(
                SiteName=SiteName,
                Latitude=Latitude,
                Longitude=Longitude,
                IslandArea=IslandArea,
                ProdFish=ProdFish,
                BoatAccessibility=boat,
                ShoreEntry=ShoreEntry,
                RTCW_Fishing=RTCW_Fishing,
                FishRank=FishRank,
                TransitTime=TransitTime,
                SMWregion=SMWregion,
                SMWprod=SMWprod,
                SMWfishing=SMWfishing,
                Notes=notes
            )

            if created:
                sts.save()

def loc_import():
    filename = 'csv_data/Locations.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            name = row['ContainerName']
            ctype = row['ContainerType']
            inst = row['Institution']
            fmp_locationID = row['pk_Location']

            loc, created = Locations.objects.get_or_create(
                ContainerType = ctype,
                ContainerName = name,
                Institution = inst,
                fmp_locationID = fmp_locationID
            )
            
            if created:
                loc.save()

def hhs_import():
    filename = 'csv_data/HHS.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            date = row['DateSurveyed']
            name = row['Names']
            fmp_hhsID = row['pk_hhsID']
            fishing = row['TypicalFishingLocation']
            village = row['Village']

            hhs, created = HHS.objects.get_or_create(
                Names = name,
                Village = village,
                FishingLocation = fishing,
                DateSurveyed = date,
                fmp_pk=fmp_hhsID
            )
            if created:
                hhs.save()

def stype_import():
    filename = 'csv_data/SampleTypes.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            pk_SampleTypeID = row['pk_SampleTypeID']
            stype = row['SampleType']
            TypeCode = row['TypeCode']

            st, created = SampleTypes.objects.get_or_create(
                SampleType=stype,
                TypeCode=TypeCode,
                #fmp_pk=pk_SampleTypeID
            )

            if created:
                st.save()

def treat_import():
    filename = 'csv_data/Treatments.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            treat = row['Treatment']
            code = row['TreatmentCode']

            treat, created = Treatments.objects.get_or_create(
                Treatment=treat,
                TreatmentCode=code
            )

            if created:
                treat.save()

def trays_import():
    filename = 'csv_data/Trays.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            tray = row['TrayName']

            tr, created = Trays.objects.get_or_create(
                TrayName=tray
            )

            if created:
                tr.save()

def state_import():
    filename = 'csv_data/SharkStates.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            State = row['State']

            s, created = SharkStates.objects.get_or_create(
                State=State
            )

            if created:
                s.save()


#### Need to clean this data because there are a lot of species that probably have typos or something.
def shmjoin_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/Fish Names Kir Eng Science Area Method.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            species = row['SpeciesCode']
            habitat = row['Place']
            method = row['Fishing Method']

            if species is None or species == '':
                continue

            # FK lookups:
            try:
                hab = FishingHabitats.objects.get(Habitat = habitat)
            except ObjectDoesNotExist as e:
                logging.warn('line: %s habitat %s %s' % 
                    (line_number, habitat, e))

            if method is None or method == '':
                pass
            else: 
                try:
                    meth = FishingMethods.objects.get(Method = method)
                except ObjectDoesNotExist as e:
                    logging.warn('line: %s method %s %s' % 
                        (line_number, method, e))

            try:
                spp = Species.objects.get(SpeciesCode = species)
                spp.Habitats.add(hab)
                spp.Methods.add(meth)
                spp.save()

            except ObjectDoesNotExist as e:
                logging.warn('spp %s does not exist' % species)

def rt2010_spec_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/RT_dissections10.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            spp = row['sp']
            OldID1 = row['old.ID.code']
            SpecimenID = row['ID.code']
            DateCollected = row['date.collected']
            Site = row['site']
            DepthCollected = row['depth.collected']
            Notes = row['notes']


            # FK lookups:
            if Site == '' or Site == 'NA':
                Site = 'Site Not Certain'

            if DepthCollected == 'NA':
                DepthCollected = None

            if spp == 'TURF':
                try:
                    sp = Species.objects.get(SpeciesCode=spp)
                    # print spp
                except ObjectDoesNotExist as e:
                    logging.warn("%s:%s spp %s does not exist" % (filename, line_number, spp
                    ))
            else:
                try:
                    site = Sites.objects.get(SiteName=Site)
                    sp = Species.objects.get(ScientificName=spp)
                
                except Exception as e:
                    logging.warn('%s:%s %s' % (filename, line_number, e))
                
            
            try:
                meth = CollectionMethods.objects.get(Method=CollectionMethod)
            except:
                meth = None


            DateCollected = shitty_date_conversion(DateCollected, blank=True)


            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    SpecimenID=SpecimenID,
                    OldID1=OldID1,
                    CollectionNotes=Notes,
                    DateCollected=DateCollected,
                    DepthCollected=DepthCollected
                )

                if created:
                    spe.save()                    

            except IntegrityError:
                logging.error("%s:%s %s is not unique" % (
                    filename, line_number, SpecimenID
                ))
            except Exception as e:
                logging.error("%s:%s Exception: %s" % (
                    filename, line_number, e
                ))

def cw1_spec_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/CW_merged_isotope_dissections2011.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 0
        for row in csvreader:
            line_number += 1
            spp = row['sp']
            OldID1 = row['cw.old.ID']
            SpecimenID = row['ID']
            DateCollected = row['date.collected']
            Site = row['site']
            DepthCollected = row['depth.ft']
            CollectionMethod = row['method']
            CollectedBy = row['collected.by']
            Notes = row['notes']
            sex = row['sex']


            # FK lookups:
            if Site == '':
                Site = 'Site Not Certain'

            try:
                site = Sites.objects.get(SiteName=Site)
                sp = Species.objects.get(ScientificName=spp)
            except Exception as e:
                logging.warn('%s:%s %s' % (filename, line_number, e))          

            try:
                meth = CollectionMethods.objects.get(Method=CollectionMethod)
            except:
                meth = None


            DateCollected = shitty_date_conversion(DateCollected, blank=True)
            
            if DepthCollected == 'NA' or DepthCollected == '?':
                DepthCollected = None
            elif DepthCollected.find('m') == -1:
                DepthCollected += 'ft'

            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    fk_Method=meth,
                    SpecimenID=SpecimenID,
                    CollectedBy=CollectedBy,
                    Sex=sex,
                    OldID1=OldID1,
                    CollectionNotes=Notes,
                    DateCollected=DateCollected,
                    DepthCollected=DepthCollected
                )

                if created:
                    spe.save()                   

            except IntegrityError:
                logging.error("%s:%s %s is not unique" % (
                    filename, line_number, SpecimenID
                ))
            except Exception as e:
                logging.error("%s:%s Exception: %s" % (
                    filename, line_number, e
                ))
                raise e

def cw2_spec_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/CW_dis_merged_2012.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 0
        for row in csvreader:
            line_number += 1
            spp = row['sp']
            SpecimenID = row['ID']
            DateCollected = row['Date collected']
            Site = row['Site']
            DepthCollected = row['Depth (ft)']
            CollectionMethod = row['Method']
            CollectedBy = row['collector']
            Notes = row['Notes']
            sex = row['Sex']

            # FK lookups:
            if Site == '':
                Site = 'Site Not Certain'

            if spp == 'Chromis margaritifer':
                Notes = Notes + ". Also note that all samples for Chromis margaritifer were lost from the Stanford freezer, so there are no subsequent processing or isotope data for these fish"

            try:
                site = Sites.objects.get(SiteName=Site)
                sp = Species.objects.get(ScientificName=spp)

                if sp is None:
                    print ('%s %s' % (line_number, spp))

            except Exception as e:
                pass
                # logging.warn('%s:%s %s' % (filename, line_number, e))

            try:
                meth = CollectionMethods.objects.get(Method=CollectionMethod)
            except:
                meth = None


            DateCollected = shitty_date_conversion(DateCollected, blank=True)
            
            if DepthCollected == 'NA' or DepthCollected =='?':
                DepthCollected = None
            elif DepthCollected.find('m') == -1:
                DepthCollected += 'ft'

            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    fk_Method=meth,
                    SpecimenID=SpecimenID,
                    CollectedBy=CollectedBy,
                    Sex=sex,
                    CollectionNotes=Notes,
                    DateCollected=DateCollected,
                    DepthCollected=DepthCollected
                )

                if created:
                    spe.save()                  

            except IntegrityError:
                continue
                #logging.error(" line: %s:%s is not unique" %
                #    (line_number, SpecimenID
                #))

            #except Exception as e:
            #    logging.error("%s:%s Exception: %s" % (
            #        filename, line_number, e
            #    ))
                #raise e

def kif11_spec_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_fish_dissections.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 0
        for row in csvreader:
            line_number += 1
            spp = row['sp.code']
            SpecimenID = row['ID']
            DateCollected = row['date.collected']
            Site = row['site']
            Notes = row['Notes']

            # FK lookups:
            if Site == '':
                Site = 'Site Not Certain'

            try:
                site = Sites.objects.get(SiteName=Site)
                sp = Species.objects.get(SpeciesCode=spp)
            except Exception as e:
                logging.warn('%s:%s %s' % (filename, line_number, e))

            if sp == False:
                print ('%s %s' % (line_number, spp))

            DateCollected = shitty_date_conversion(DateCollected, blank=True)

            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    SpecimenID=SpecimenID,
                    CollectionNotes=Notes,
                    DateCollected=DateCollected
                )
                
                if created:
                    spe.save()                  

            except IntegrityError:
                logging.error(" line: %s:%s is not unique" %
                    (line_number, SpecimenID
                ))
                #logging.error("%s:%s %s is not unique" % (
                #    filename, line_number, SpecimenID
                #))
            #except Exception as e:
            #    logging.error("%s:%s Exception: %s" % (
            #        filename, line_number, e
            #    ))
                #raise e

def kif12_spec_import(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2012_Kiritimati_field_fish_dissections.csv'):
    
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            spp = row['species']
            SpecimenID = row['ID.code']
            DateCollected = row['date.collected']
            Site = row['site']
            Notes = row['notes']

            # FK lookups:
            if Site == '':
                Site = 'Site Not Certain'

            try:
                site = Sites.objects.get(SiteName=Site)
                sp = Species.objects.get(SpeciesCode=spp)

            except Exception as e:
                logging.warn('%s:%s %s %s' % (filename, line_number, spp, e))


            DateCollected = shitty_date_conversion(DateCollected, blank=True)


            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    SpecimenID=SpecimenID,
                    CollectionNotes=Notes,
                    DateCollected=DateCollected
                )

                if created:
                    spe.save()                  

            except IntegrityError:
                logging.error(" line: %s:%s is not unique" %
                    (line_number, SpecimenID
                ))

            #except Exception as e:
            #    logging.error("%s:%s Exception: %s" % (
            #        filename, line_number, e
            #    ))
                #raise e

def bz_fish_spec(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/Zgliczynski_SampleIndex.csv'):

    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            spp = row['Species']
            SpecimenID = row['code']
            Notes = row['Specimen Notes']

            # FK lookups:
            site = 'Site Not Certain'

            try:
                site = Sites.objects.get(SiteName=site)
                sp = Species.objects.get(SpeciesCode=spp)

            except Exception as e:
                logging.warn('%s:%s %s %s' % (filename, line_number, spp, e))

            # assigning values:
            try: 
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    SpecimenID=SpecimenID,
                    CollectionNotes=Notes
                )

                if created:
                    spe.save()

            except IntegrityError:
                logging.error(" line: %s:%s is not unique" %
                    (line_number, SpecimenID
                ))

def PP_2011_spec(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_PP_collections2.csv'):
    
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            spp = row['SpeciesCode']
            SpecimenID = row['ID.code']
            DateCollected = row['date.collected']
            Site = row['site']
            Notes = row['notes']

            # FK lookups:
            if Site == '' or Site == 'NA':
                Site = 'Site Not Certain'

            try:
                site = Sites.objects.get(SiteName=Site)
                sp = Species.objects.get(SpeciesCode=spp)

            except Exception as e:
                logging.warn('%s %s %s' % (line_number, spp, e))


            DateCollected = shitty_date_conversion(DateCollected, blank=True)


            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=sp,
                    SpecimenID=SpecimenID,
                    CollectionNotes=Notes,
                    DateCollected=DateCollected
                )

                if created:
                    spe.save()                  

            except IntegrityError:
                logging.error(" line: %s:%s is not unique" %
                    (line_number, SpecimenID
                ))

            #except Exception as e:
            #    logging.error("%s:%s Exception: %s" % (
            #        filename, line_number, e
            #    ))
                #raise e

def Uvic_PP_import(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/UVICmacroprepping_sheet_data_WORKING_COPY_May24.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['ID']
            species = row['Species']
            site = row['Site']

            specimen_id = sample_id[0:8]

        # FK lookups:
            species = Species.objects.get(SpeciesCode=species)
            site = Sites.objects.get(SiteName=site)

        # assigning values:
            pp, created = Specimens.objects.get_or_create(
                SpecimenID=specimen_id,
                fk_Species=species,
                fk_Site=site
            )

            if created:
                pp.save()


def dis_import_RT10(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/RT_dissections10.csv'):

    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            specimenID = row['ID.code']
            # get specimen here

            try:
                specimen = Specimens.objects.get(SpecimenID=specimenID)
            except Exception as e:
                logging.error("%s:%s Exception: %s" % (
                    filename, line_number, e
                ))

            date_dissected = row['DateDissected']
            dissected_by = row['DissectedBy']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            gh = row['gh']
            gw = row['gw']
            wt = row['wt']
            notes = row['notes']
            oto = row['OtolithSample']
            prey_size = row['PreySizeInStomach']
            stomach_contents = row['StomachContents']
            #stomach_sample = row['stom.sample']



            if fl == '' or fl == 'NA': fl = None
            if gh == '' or gh == 'NA': gh = None
            if gw == '' or gw == 'NA': gw = None
            if sl == '' or sl == 'NA': 
                sl = None
                #print '%s, %s no standard length' % (line_number, specimen)
            if tl == '' or tl == 'NA': 
                tl = None
                #print '%s, %s no total length' % (line_number, specimen)
            if wt == '' or wt == 'NA': 
                wt = None
                #print '%s, %s no weight' % (line_number, specimen)
            if date_dissected == '': date_dissected = None
            elif date_dissected == 'NA': date_dissected = None


            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    gh=gh,
                    gw=gw,
                    DateDissected=date_dissected,
                    #StomachSample=stomach_sample,
                    StomachContents=stomach_contents,
                    PreySize=prey_size,
                    OtolithSample=oto,
                    DissectedBy=dissected_by,
                    Notes=notes
                )

                if created:
                    dis.save()
            except Exception as e:
                logging.error("%s:%s %s" % (filename, line_number, e))

def dis_import_CW1(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/CW_merged_isotope_dissections2011.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            specimenID = row['ID']
            # get specimen here

            try:
                specimen = Specimens.objects.get(SpecimenID=specimenID)
            except Exception as e:
                logging.error("%s:%s Exception: %s" % (
                    filename, line_number, e
                ))

            DateDissected = row['DateDissected']
            GonadsRipe = row['gonads.ripe']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            wt = row['wt']
            notes = row['notes']
            StomachContents = row['StomachContents']
            Intestines = row['intestine']

            if Intestines != 'NA':
                StomachContents += '. Intestines: %s' % Intestines

            DateDissected = shitty_date_conversion(DateDissected, blank=True)

            if fl == '' or fl == 'NA': fl = None
            #if gh == '' or gh == 'NA': gh = None
            #if gw == '' or gw == 'NA': gw = None
            if sl == '' or sl == 'NA': 
                sl = None
                #print '%s, %s no standard length' % (line_number, specimen)
            if tl == '' or tl == 'NA': 
                tl = None
                #print '%s, %s no total length' % (line_number, specimen)
            if wt == '' or wt == 'NA': 
                wt = None
                #print '%s, %s no weight' % (line_number, specimen)
            if DateDissected == '': DateDissected = None
            elif DateDissected == 'NA': DateDissected = None

            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    DateDissected=DateDissected,
                    StomachContents=StomachContents,
                    Notes=notes,
                    GonadsRipe=GonadsRipe
                )

                if created:
                    dis.save()
            except Exception as e:
                logging.error("%s:%s %s" % (filename, line_number, e))

def dis_import_CW2(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/CW_dis_merged_2012.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            specimenID = row['ID']
            # get specimen here

            try:
                specimen = Specimens.objects.get(SpecimenID=specimenID)
            except Exception as e:
                pass
                #logging.error("%s Exception: %s" % (line_number, e))

            DateDissected = row['DateDissected']
            GonadsRipe = row['gonads.ripe']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            wt = row['wt']
            Notes = row['Notes']
            StomachContents = row['StomachContents']
            Intestines = row['intestine']
            units = row['length.units']

            if Intestines != 'NA':
                StomachContents += '. Intestines: %s' % Intestines

            DateDissected = shitty_date_conversion(DateDissected, blank=True)

            if fl == '' or fl == 'NA': 
                fl = None
            elif units == 'mm':
                fl = fl
            elif units == 'in':
                fl = float(fl)*25.4
            elif units == 'cm':
                fl = float(fl)*10.0

            if sl == '' or sl == 'NA': 
                sl = None
            elif units == 'mm':
                sl = sl
            elif units == 'in':
                sl = float(sl)*25.4
            elif units == 'cm':
                sl = float(sl)*10.0

            if tl == '' or tl == 'NA': 
                tl = None
            elif units == 'mm':
                tl = tl
            elif units == 'in':
                tl = float(tl)*25.4
            elif units == 'cm':
                tl = float(tl)*10.0

            if wt == '' or wt == 'NA': 
                wt = None
            
            #    try:
             #       tl = float(tl)*25.4
              #      fl = float(fl)*25.4
               #     sl = float(sl)*25.4
                #except TypeError as e:
                 #   print '%s %s' % (line_number, e)



            if DateDissected == '': DateDissected = None
            elif DateDissected == 'NA': DateDissected = None

            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    DateDissected=DateDissected,
                    StomachContents=StomachContents,
                    Notes=Notes,
                    GonadsRipe=GonadsRipe
                )

                if created:
                    dis.save()
            except Exception as e:
                pass
                #logging.error("%s:%s %s" % (filename, line_number, e))

def dis_import_KI11(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_fish_dissections.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            specimenID = row['ID']
            # get specimen here

            try:
                specimen = Specimens.objects.get(SpecimenID=specimenID)
            except Exception as e:
                #pass
                logging.error("%s Exception: %s" % (line_number, e))

            date_dissected = row['DateDissected']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            wt = row['wt']
            gh = row['gh']
            gw = row['gw']
            notes = row['Notes']
            stomach_contents = row['StomachContents']
            prey_size = row['PreySize']
            oto = row['oto.sample']
            photo_name = row['photo']
            iso = row['iso.sample']
            dissected_by = row['DissectedBy']
            stomach_sample = row['stom.sample']

            date_dissected = shitty_date_conversion(date_dissected, blank=True)

            if fl == '' or fl == 'NA': 
                fl = None

            if sl == '' or sl == 'NA': 
                sl = None

            if tl == '' or tl == 'NA': 
                tl = None

            if wt == '' or wt == 'NA': 
                wt = None
            
            if gh == '' or gh == 'NA':
                gh = None

            if gw == '' or gw == 'NA':
                gw = None

            #    try:
             #       tl = float(tl)*25.4
              #      fl = float(fl)*25.4
               #     sl = float(sl)*25.4
                #except TypeError as e:
                 #   print '%s %s' % (line_number, e)

            if date_dissected == '': date_dissected = None
            elif date_dissected == 'NA': date_dissected = None

            if stomach_sample == 'Y':
                stomach_sample = True
            elif stomach_sample == 'N':
                stomach_sample = False
            elif stomach_sample == '':
                stomach_sample = None

            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    gh=gh,
                    gw=gw,
                    PreySize=prey_size,
                    OtolithSample=oto,
                    PhotoName=photo_name,
                    IsotopeSample=iso,
                    DateDissected=date_dissected,
                    StomachContents=stomach_contents,
                    Notes=notes,
                    DissectedBy=date_dissected,
                    StomachSample=stomach_sample
                )

                if created:
                    dis.save()
            except Exception as e:
                logging.error("%s:%s %s" % (filename, line_number, e))

                logging.error('line %s: skipping %s' % (line_number, SampleID))
                continue


def dis_import_KI12(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2012_Kiritimati_field_fish_dissections.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            specimenID = row['ID.code']
            # get specimen here

            try:
                specimen = Specimens.objects.get(SpecimenID=specimenID)
            except Exception as e:
                #pass
                logging.error("%s Exception: %s" % (line_number, e))

                logging.error('line %s: skipping %s' % (line_number, SampleID))
                continue

            date_dissected = row['DateProcessed']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            wt = row['wt']
            gh = row['gh']
            gw = row['gw']
            notes = row['notes']
            stomach_contents = row['StomachContents']
            prey_size = row['PreySize']
            oto = row['otoliths']
            iso = row['iso.sample']
            dissected_by = row['DissectedBy']
            spp = row['species']
            stomach_sample = row['stom.sample']

            date_dissected = shitty_date_conversion(date_dissected, blank=True)

            if fl == '' or fl == 'NA': 
                fl = None

            if sl == '' or sl == 'NA': 
                sl = None

            if tl == '' or tl == 'NA': 
                tl = None

            if gh == '' or gh == 'NA':
                gh = None

            if gw == '' or gw == 'NA':
                gw = None

            if wt == '' or wt == 'NA': 
                wt = None
            elif wt.find('lb') != -1:
                notes += ". Original recorded weight: %s" % wt
                wt_num = wt.translate(None, 'lbs')
                wt = float(wt_num)*454

            if stomach_sample == 'Y':
                stomach_sample = True

            elif stomach_sample == 'N':
                stomach_sample = False

            elif stomach_sample == '':
                stomach_sample = None
            
            #    try:
             #       tl = float(tl)*25.4
              #      fl = float(fl)*25.4
               #     sl = float(sl)*25.4
                #except TypeError as e:
                 #   print '%s %s' % (line_number, e)

            #if date_dissected == '': DateDissected = None
            #elif DateDissected == 'NA': DateDissected = None

            if stomach_sample == 'N':
                Notes += '. No stomach sample taken.'

            if spp not in ['SHARK.SP', 'CA.MELAN', 'CA.AMBL']:
     
                try:
                    dis, created = Dissections.objects.get_or_create(
                        fk_Specimen = specimen,
                        TL=tl,
                        FL=fl,
                        SL=sl,
                        wt=wt,
                        gh=gh,
                        gw=gw,
                        PreySize=prey_size,
                        OtolithSample=oto,
                        IsotopeSample=iso,
                        DateDissected=date_dissected,
                        StomachContents=stomach_contents,
                        Notes=notes,
                        DissectedBy=dissected_by,
                        StomachSample = stomach_sample
                    )

                    if created:
                        dis.save()
                except Exception as e:
                    logging.error("%s:%s %s" % (filename, line_number, e))


def samp_import(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/KI_SI_sample_Index.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            SpecimenID = row['SpecimenID']
            SampleID = row['SampleID']
            OldSampleID = row['code']
            SampleType = row['sample type']
            Notes = row['sample notes']


        # Skip blank rows:
            if SampleID is None or SampleID == '':
                continue

        # FK lookup:
            try:
                specimen = Specimens.objects.get(SpecimenID=SpecimenID)
            except ObjectDoesNotExist as e:
                logging.warn('line %s specimen %s does not exist' 
                    % (line_number, SpecimenID))
                
                # go on to the next sample
                logging.error('line %s: skipping %s' % (line_number, SampleID))
                continue

            try:
                stype = SampleTypes.objects.get(TypeCode=SampleType)
            except ObjectDoesNotExist as e:
                logging.warn('line %s stype %s does not exist' 
                    % (line_number, SampleType))

        # assigning values:
            try:
                samp, created = Samples.objects.get_or_create(
                    fk_Specimen=specimen,
                    fk_SampleType=stype,
                    SampleID=SampleID,
                    OldSampleID=OldSampleID,
                    Notes=Notes
                )
                
                if created:
                    samp.save()

            except IntegrityError as e:
                    logging.warn("line: %s Duplicate SampleID: %s" % 
                        (line_number, SampleID))



def samp_locations(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/KI_SI_sample_Index.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample = row['SampleID']
            ContainerType = row['Box type']
            ContainerName = row['dried box number']
            Institution = row['Location']

        # FK lookups:
            try:
                sample = Samples.objects.get(SampleID=sample)

            except ObjectDoesNotExist as e:
                logging.warn('line %s: location: %s does not exist' % (line_number, sample))
                logging.error('line %s: skipping %s' % (line_number, sample))
                continue

            try:
                location = Locations.objects.get(
                    ContainerType=ContainerType,
                    ContainerName=ContainerName,
                    Institution=Institution
                    )
            except ObjectDoesNotExist as e:
                #logging.warn('line %s Location %s:%s:%s does not exist' 
                 #   % (line_number, ContainerType, ContainerName, Institution))
                continue

            sl, created = SampleLocations.objects.get_or_create(
                fk_Sample=sample,
                fk_Location=location
                )


def spares_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/KI_SI_sample_Index.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            SpecimenID = row['SpecimenID']
            Container = row['spare location']
            Institution = 'UVic'

        # FK lookup:
            try:
                SpecimenID = Specimens.objects.get(SpecimenID=SpecimenID)

            except ObjectDoesNotExist as e:
                logging.warn('line %s specimen %s does not exist' 
                    % (line_number, SpecimenID))
                continue

            s, created = SpecimenSpareSamples.objects.get_or_create(
                fk_Specimen=SpecimenID,
                Container=Container,
                Institution=Institution
                )

            if created:
                s.save()


def state_import():
    filename = 'csv_data/SharkStates.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            State = row['State']

            s, created = SharkStates.objects.get_or_create(
                State=State
            )

            if created:
                s.save()


def piece_import():
    filename = 'csv_data/SharkPieces.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            piece = row['SharkPiece']

            sps, created = SharkPieces.objects.get_or_create(
                SharkPiece=piece
            )

            if created:
                sps.save()


def shark_spec_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/KIR2012 - filtering, outreach, surveys.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            site_name = 'No site: see household surveys'
            species = row['Sample Species']
            specimen_id = row['Sample ID']
            hhs_name = row['Names']
            village = row['Village']
            date_surveyed = row['Date Surveyed/Collected']
            collection_notes = row['Notes']

            date_surveyed = shitty_date_conversion(date_surveyed)

            if collection_notes is None or collection_notes != '':
                pass
            else:
                collection_notes = collection_notes + ". "

            collection_notes = collection_notes + "Shark specimens do not necessarily represent individual specimens. In some cases, fins are identified as being from the same specimen but in most cases it was not possible to identify a complete set of fins as being from a single shark. Most dorsal fins and tail fins are recorded as individual specimens although they come from the same specimens as some of the pectoral fin sets."

            try:
                site = Sites.objects.get(SiteName = site_name)
                spp = Species.objects.get(SpeciesCode = species)
                hhs = HHS.objects.get(
                    Names = hhs_name,
                    Village = village,
                    DateSurveyed = date_surveyed
                    )

                print spp.SpeciesCode

            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s does not exist' % (line_number, e))


            try:
                spec, created = Specimens.objects.get_or_create(
                    fk_Site = site,
                    fk_Species = spp,
                    SpecimenID = specimen_id,
                    CollectionNotes = collection_notes
                    )

                if created:
                    spec.save()

            except IntegrityError as e:
                logging.warn("line: %s specimen %s %s" % 
                    (line_number, specimen_id, e))
            try:
                spec_id = Specimens.objects.get(SpecimenID = specimen_id)

            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s' % (line_number, e))
            

            try:
                sh_spec, created = SharkSpecimens.objects.get_or_create(
                    fk_SpecimenID = spec_id,
                    fk_HHS = hhs
                    )

                if created:
                    sh_spec.save()

            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s' % (line_number, e))

def sharkdis_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/shark_dissections.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            specimen = row['sampleID']
            pcl = row['pcl']
            fl = row['fl']
            tl = row['tl']
            stretch = row['stretch']
            dh = row['dorsal ht']
            db = row['dorsal base']
            ph = row['pectoral ht']
            pb = row['pectoral base']
            th = row['tail fin ht']
            tb = row['tail fin base']
            wt = row['Weight (lbs)']
            photo = row['Photo Taken']
            notes = row['Notes']
            date = row['Date Surveyed/Collected']

            date_dissected = shitty_date_conversion(date)

        # Fk lookups:
            specimen = Specimens.objects.get(SpecimenID=specimen)

            sds, created = SharkDissections.objects.get_or_create(
                fk_Specimen=specimen,
                PCL=pcl,
                FL=fl,
                TL=tl,
                stretch=stretch,
                DH=dh,
                DB=db,
                PH=ph,
                PB=pb,
                TH=th,
                TB=tb,
                wt=wt,
                PhotoTaken=photo,
                Notes=notes,
                DateDissected=date_dissected
            )

            if created:
                sds.save()

def shark_samp_prep_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/MW_DirectedStudies_SharkSamples.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            specimen = row['SpecimenID_lookup']
            sample_type = row['Sample Type']
            old_spec = row['old_SpecimenID']
            sample_id = row['SampleID']
            notes = row['Notes']
            old_samp = row['Old Sample ID']
            date_dissected = row['Date Dissected']
            piece = row['Sample Location']
            state = row['State']
            treatment = row['Treatment']
            date_wash_dry = row['Date Rinsed/Put in Drier']
            prepped_by = row['Prepped By']
            date_ground = row['Ground']
            drying_method = row['DryingMethod']
            drying_hours = row['DryingHours']

            date_dis = shitty_date_conversion(date_dissected)
            date_wd = shitty_date_conversion(date_wash_dry, blank = True)
            date_ground = shitty_date_conversion(date_ground, blank = True)


            if old_samp is None or old_samp == '':
                old_sample_id = old_spec + '_' + sample_id
            else:
                old_sample_id = old_spec + '_' + old_samp

        # SAMPLES Import:
            try:
                spec = Specimens.objects.get(SpecimenID = specimen)

            except ObjectDoesNotExist as e:
                logging.warn("line: %s, %s %s" % (line_number, specimen, e))

            try:
                stype = SampleTypes.objects.get(TypeCode = sample_type)
            
            except ObjectDoesNotExist as e:
                logging.warn("line: %s, %s %s" % (line_number, sample_type, e))


            try:
                samp, created = Samples.objects.get_or_create(
                    fk_Specimen = spec,
                    fk_SampleType = stype,
                    OldSampleID = old_sample_id,
                    SampleID = sample_id,
                    Notes = notes
                    )
                
                if created:
                    samp.save()

            except IntegrityError as e:
                logging.warn("line: %s sample %s %s" % 
                    (line_number, sample_id, e))

        # SHARK SAMPLES Import:
            try:
                piece = SharkPieces.objects.get(SharkPiece = piece)
            except ObjectDoesNotExist as e:
                logging.warn("line: %s piece %s %s" %(line_number, piece, e))

            try:
                samp = Samples.objects.get(SampleID = sample_id)
            except ObjectDoesNotExist as e:
                logging.warn("line: %s sample %s %s" % 
                    (line_number, sample_id, e))

            try:
                state = SharkStates.objects.get(State = state)
            except ObjectDoesNotExist as e:
                logging.warn("line: %s state %s %s" % (line_number, state, e))

            try:
                ss, created = SharkSamples.objects.get_or_create(
                    fk_Sample = samp,
                    fk_SharkPiece = piece,
                    fk_State = state,
                    DateDissected = date_dis
                    )

                if created:
                    ss.save()

            except IntegrityError as e:
                logging.warn("line: %s sample %s %s" % 
                    (line_number, sample_id, e))

        # PREP import
            if treatment or treatment != '':
                treat = Treatments.objects.get(TreatmentCode = treatment)

                prep, created = Preprocessings.objects.get_or_create(
                    fk_Sample = samp,
                    fk_Treatment = treat,
                    DateWashDry = date_wd,
                    PreppedBy = prepped_by,
                    PrepEntered = prepped_by,
                    DateGround = date_ground,
                    DryingMethod = drying_method,
                    DryingTime = drying_hours
                    )

                if created:
                    prep.save()


def prep_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/consolidated_preprocessing.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['ID']
            date_wash_dry = row['date.rinsed']
            treatment = row['decarb']
            prepped_by = row['processed.by']
            drying_method = row['drying method']
            drying_time = row['drying.hours']
            entered_by = row['entered.by']
            notes = row['notes']

            if sample_id is None or sample_id == '':
                continue

        # FK lookups:
            try:
                sample = Samples.objects.get(SampleID=sample_id)
                #if created:
                 #   print('sample created: %s' % sample_id)

            except ObjectDoesNotExist as e:
                logging.warn('line %s: Sample: %s does not exist' 
                    % (line_number, sample_id))
                continue

            try:
                treatment = Treatments.objects.get(TreatmentCode=treatment)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: treatment "%s" does not exist' 
                    % (line_number, treatment))
                #continue

        # Fix shitty date formats:
            date_wash_dry = shitty_date_conversion(date_wash_dry, blank=True)

        # assigning values:
            try:
                prep, created = Preprocessings.objects.get_or_create(
                    fk_Sample=sample,
                    fk_Treatment=treatment,
                    DateWashDry=date_wash_dry,
                    PreppedBy=prepped_by,
                    PrepEntered=entered_by,
                    DryingMethod=drying_method,
                    DryingTime=drying_time,
                    Notes=notes
                )

                if created:
                    prep.save()
            except IntegrityError as e:
                logging.warn("line: %s fk_Sample is not unique: %s" % (line_number, sample_id))

def ki_2011_pp_prep_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_PP_preprocessing_treatment.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            spec_id = row['ID.code']
            date_wash_dry = row['date.processed']
            sample_id = row['SampleID']
            treatment = row['treatment']
            label = row['treatment label']
            sample_type = row['Sample Type']
            prep_notes = row['notes']
            sample_notes = row['sample_notes']


            date_wd = shitty_date_conversion(date_wash_dry, blank=True)

            old_sample_id = spec_id + '_' + label

            # skip blank lines/blank sampleIDs (missing ones... still trying to
                # resolve)
            if sample_id is None or sample_id == '':
                continue

        # Sample lookup or creation:
            try:
                sample = Samples.objects.get(SampleID = sample_id)

            except ObjectDoesNotExist as e:
                #logging.warn('line %s: Sample: %s does not exist' 
                 #   % (line_number, sample_id))
                #sample = None

                if e:

            # Sample creation lookups:
                    try:
                        specimen = Specimens.objects.get(SpecimenID = spec_id)
                        stype = SampleTypes.objects.get(TypeCode = sample_type)

                        s, created = Samples.objects.get_or_create(
                            SampleID = sample_id,
                            fk_Specimen = specimen,
                            fk_SampleType =  stype,
                            Notes = sample_notes
                            )

                        if created:
                            print('sample created: %s' % sample_id)
                            s.save()

                    except ObjectDoesNotExist as e:
                        logging.warn('line %s: Specimen: "%s" %s' 
                            % (line_number, spec_id, e))


        # Prep FK lookups:
            try:
                treatment = Treatments.objects.get(TreatmentCode=treatment)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: treatment "%s" does not exist' 
                    % (line_number, treatment))

            try:
                prep, created = Preprocessings.objects.get_or_create(
                    fk_Sample = sample,
                    fk_Treatment = treatment,
                    DateWashDry = date_wd,
                    Notes = prep_notes
                    )

                if created:
                    prep.save()

            except IntegrityError, e:
                logging.warn('line %s: sampleID %s %s' % 
                    (line_number, sample_id, e))

def uvic_prep_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/UVICmacroprepping_sheet_data_WORKING_COPY_May24.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['ID']
            date_wash_dry = row['Prep date']
            date_ground = row['Grinding date']
            treatment = row['Treatment-A/NA/R']
            drying_method = row['drying method']
            drying_time = row['drying time']
            sample_type = row['sample type']

            specimen_id = sample_id[0:8]
        # Date cleanup:
            date_wash_dry = shitty_date_conversion(date_wash_dry, blank=True)
            date_ground = shitty_date_conversion(date_ground, blank=True)


        # FK lookups:
            try:
                specimen = Specimens.objects.get(SpecimenID=specimen_id)
                stype = SampleTypes.objects.get(TypeCode=sample_type)
                
                sample, created = Samples.objects.get_or_create(
                    SampleID=sample_id,
                    fk_Specimen=specimen,
                    fk_SampleType=stype
                    )

                if created:
                    sample.save()

            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s %s' 
                    % (line_number, sample_id, e))
                continue

            try:
                treatment = Treatments.objects.get(TreatmentCode=treatment)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s does not exist' 
                    % (line_number, sample_id))
                continue

        # assigning values:

            try:
                prep, created = Preprocessings.objects.get_or_create(
                    fk_Sample=sample,
                    fk_Treatment=treatment,
                    DateWashDry=date_wash_dry,
                    DryingMethod=drying_method,
                    DryingTime=drying_time
                )

                if created:
                    prep.save()
            except IntegrityError as e:
                logging.warn("line: %s fk_Sample is not unique: %s" % (line_number, sample))

def BZ_prep_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/Zgliczynski_SampleIndex.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['code']
            treatment = row['Treatment']

            sample = Samples.objects.get(SampleID = sample_id)
            treat = Treatments.objects.get(TreatmentCode = treatment)

            prep, created = Preprocessings.objects.get_or_create(
                fk_Sample = sample,
                fk_Treatment = treat
                )

            if created:
                prep.save()

def uvic_FISH_prep_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/New_Fish Prep Data Entry Sheet.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['SampleID']
            date_wash_dry = row['Rinsing Date: yyyy-mm-dd']
            date_ground = row['Grinding Date yyyy-mm-dd']
            treatment = row['Treatment']
            drying_method = row['Drying method']
            drying_time = row['Drying time (hours)']
            specimen_id = row['Specimen ID']
            sample_type = row['SampleType']
            by = row["PreppedBy"]
            entered = row['EnteredBy']
            notes = row["Notes"]


        # Date cleanup:
            date_wash_dry = shitty_date_conversion(date_wash_dry, blank=True)
            date_ground = shitty_date_conversion(date_ground, blank=True)


        # FK lookups:
            try:
                specimen = Specimens.objects.get(SpecimenID=specimen_id)
                stype = SampleTypes.objects.get(SampleType=sample_type)
                
                sample, created = Samples.objects.get_or_create(
                    SampleID=sample_id,
                    fk_Specimen=specimen,
                    fk_SampleType=stype
                    )

                if created:
                    sample.save()

            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s does not exist' 
                    % (line_number, e))
                continue

            try:
                treatment = Treatments.objects.get(TreatmentCode=treatment)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s does not exist' 
                    % (line_number, sample_id))
                continue

        # assigning values:

            try:
                prep, created = Preprocessings.objects.get_or_create(
                    fk_Sample=sample,
                    fk_Treatment=treatment,
                    DateWashDry=date_wash_dry,
                    DryingMethod=drying_method,
                    DryingTime=drying_time,
                    DateGround=date_ground,
                    PreppedBy=by,
                    PrepEntered=entered,
                    Notes=notes,
                )

                if created:
                    prep.save()
            except IntegrityError as e:
                logging.warn("line: %s fk_Sample is not unique: %s" % (line_number, sample))


def uvic_2011_packed_import():
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/UVICpacking_sheet_data_WORKING_COPY2.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['ID_code']
            tray_name = row['tray_no']
            trow = row['row']
            col = row['column']
            cap_wt = row['Cap Weight']
            filled_wt = row['Cap and sample weight']
            sample_wt = row['wt.mg']
            packed_by = row['by']
            entered_by = row['entered_by']
            date_packed = row['date.packed']
            notes = row['notes']
            sample_type = row['sample_type']

            if sample_type == 'STANDARD':
                continue

            good_date_packed = shitty_date_conversion(date_packed, blank=True)

            try:
                sample = Samples.objects.get(SampleID=sample_id)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s %s' % (line_number, sample_id, e))

            try:
                tray = Trays.objects.get(TrayName=tray_name)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s %s' % (line_number, tray_name, e))


            if cap_wt.strip() == '':
                cap_wt = None

            if filled_wt.strip() == '':
                filled_wt = None


        # importing data into table:
            try:
                ps, created = PackedSamples.objects.get_or_create(
                    fk_Sample = sample,
                    fk_TrayName = tray,
                    TrayRow = trow,
                    TrayColumn = col,
                    CapWeight = cap_wt,
                    FilledCapWeight = filled_wt,
                    SampleWeight = sample_wt,
                    PackedBy = packed_by,
                    EnteredBy = entered_by,
                    DatePacked = good_date_packed,
                    Notes = notes
                )

                if created:
                    ps.save()

            except IntegrityError as e:
               logging.warn("line: %s tray_name and position is not unique: %s %s%s" % (line_number, tray_name, trow, col))

            except Exception as e:
                logging.warn("error %s: in line: %s " % (e, line_number))

def sfu_packed_import():
    #PackedSamples.objects.all().delete()
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/sfu_packing_sheet_data_working_copy.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['sample_ID']
            tray_name = row['tray_no']
            tray_row = row['row']
            tray_column = row['column']
            sample_weight = row['wt_mg']
            packed_by = row['by']                      
            entered_by = row['entered_by']
            date_packed = row['date.packed']
            notes = row['notes']

        # Fixing shitty dates:
            date_packed = shitty_date_conversion(date_packed, blank=True)

        # FK lookups:
            try:
                sample = Samples.objects.get(SampleID=sample_id)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s does not exist' % 
                    (line_number, sample_id))

            try:
                tray = Trays.objects.get(TrayName=tray_name)
            except ObjectDoesNotExist as e:
                logging.warn('line %s: %s does not exist' % 
                    (line_number, tray_name))

            if sample_weight.strip() == '':
                sample_weight = None

        # importing data into table:
            try:
                ps, created = PackedSamples.objects.get_or_create(
                    fk_Sample = sample,
                    fk_TrayName = tray,
                    TrayRow = tray_row,
                    TrayColumn = tray_column,
                    SampleWeight = sample_weight,
                    PackedBy = packed_by,
                    EnteredBy = entered_by,
                    DatePacked = date_packed,
                    Notes = notes
                )

                if created:
                    ps.save()

            except IntegrityError as e:
               logging.warn("line: %s tray_name and position is not unique: %s %s%s" % (line_number, tray_name, tray_row, tray_column))

            except Exception as e:
                logging.warn("error %s: in line: %s " % (e, line_number))

def uvic_2012_packed_import():
    #PackedSamples.objects.filter(id__gt = 1780).delete()
    filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/New_SI Packing Sheet_May23.csv'    
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 1
        for row in csvreader:
            line_number += 1
            sample_id = row['SampleID']
            new_shark = row['MW sample ID update']
            tray_name = row['Tray Number']
            cap_wt = row['Capsule weight (mg)']
            filled_wt = row['Cap and Sample weight (mg)']
            sample_wt = row['Sample Weight (mg)']
            tray_row = row['Row']
            tray_col = row['Column']
            date_packed = row['Date packed yyyy-mm-dd']
            packed_by = row['PackedBy']
            notes = row['Notes']


            if (sample_id is None or sample_id == '') and (new_shark is None or new_shark == '') or sample_id == "STANDARD":
                continue
            else:

                date_packed = shitty_date_conversion(date_packed, blank = True)

            # FK lookups:
                try:
                    if new_shark is None or new_shark == '':
                        sample = Samples.objects.get(SampleID = sample_id)

                    else:
                        sample_id = new_shark
                        sample = Samples.objects.get(SampleID = sample_id)
                        

                except ObjectDoesNotExist as e:
                    logging.warn("line: %s, %s %s" % 
                        (line_number, sample_id, e))

                try:
                    tray = Trays.objects.get(TrayName=tray_name)
                except ObjectDoesNotExist as e:
                    logging.warn('line %s: %s does not exist' % 
                        (line_number, tray_name))
                
                try:
                    ps, created = PackedSamples.objects.get_or_create(
                        fk_Sample = sample,
                        fk_TrayName = tray,
                        TrayRow = tray_row,
                        TrayColumn = tray_col,
                        CapWeight = cap_wt,
                        FilledCapWeight = filled_wt,
                        SampleWeight = sample_wt,
                        PackedBy = packed_by,
                        DatePacked = date_packed,
                        Notes = notes
                    )

                    if created:
                        ps.save()

                except IntegrityError as e:
                   logging.warn("line: %s tray_name and position is not unique: %s %s%s" % 
                    (line_number, tray_name, tray_row, tray_column))

                except Exception as e:
                    logging.warn("error %s: in line: %s " % (e, line_number))


def results_import(filename = "/Users/jillian/Dropbox/Stable isotope database/input_data/SI Results/consolidated_sfu_results.csv"):
    #Results.objects.all().delete()
    print filename
    with open(filename, 'rU') as csvfile:
            csvreader = csv.DictReader(csvfile)
            line_number = 1
            for row in csvreader:
                line_number += 1
                tray_name = row['tray_name']
                sample_id = row['sample_id']
                tray_position = row['tray_position']
                dC13 = row['dC13']
                dN15 = row['dN15']
                lab = row['lab']

                trow = tray_position[0]
                tcol = int(tray_position[1:])

                try:
                    sample = Samples.objects.get(SampleID = sample_id)
                except ObjectDoesNotExist as e:
                    logging.warn("line %s: %s %s" % (line_number, sample_id, e))

                try:
                    tray = Trays.objects.get(TrayName = tray_name)
                except ObjectDoesNotExist as e:
                    logging.warn("line %s: %s %s" % (line_number, sample_id, e))

                try:
                    packed = PackedSamples.objects.get(
                        fk_Sample = sample,
                        fk_TrayName = tray,
                        TrayRow = trow,
                        TrayColumn = tcol
                        )
                except ObjectDoesNotExist as e:
                    logging.warn("line %s: %s %s" % (line_number, sample_id, e))

                try:
                    result, created = Results.objects.get_or_create(
                        fk_Packed = packed,
                        d13C = dC13,
                        d15N = dN15,
                        Lab = lab
                        )

                    if created:
                        result.save()
                except IntegrityError as e:
                    logging.warn("line %s: sample %s %s" % (line_number, sample_id, e))

                except ValidationError as e:
                    logging.warn("line %s: sample %s %s" % (line_number, sample_id, e))


# dirty dirty dirty
def main():
    # build the path to the sqlite db
    db = os.path.join(os.getcwd(), "db/sqlite3.db")

    # delete the database file
    call(["rm %s" % db], shell=True)

    # recreate the database so all tables are present but empty
    call("python manage.py syncdb --noinput", shell=True)

    print ' > Collection Methods'
    cm_import()

    print ' > All FishingHabitats'
    fh_import()
    
    #All FishingMethods imported from FMP csv with 0 errors
    print ' > Fishing Methods'
    fm_import()
    
    #All Waypoints imported from FMP csv with 0 errors
    print ' > Waypoints'
    wp_import()
    
    #All FunctionalGroups imported from FMP csv with 0 errors
    print ' > FunctionalGroups'
    fg_import()
    
    #All LengthWeights imported from FMP csv with 0 errors
    print ' > LengthWeights'
    lw_import()
    #lw_import(filename = 'Users/jillian/Dropbox/Stable isotope database/csv_data/Lengthweights.csv')
    # not sure if I need the .csv extension

    print ' > SpeciesTypes'
    sp_type()

    print ' > Species'
    sp_import()
    #sp_import(filename = 'Users/jillian/Dropbox/Stable isotope database/csv_data/Taxonomies.csv')
    # not sure if I need the .csv extension

    print ' > Sites'
    sites_import()

    print ' > Locations'
    # locations
    loc_import()

    print ' > HHS'
    hhs_import()

    print ' > Sample Types'
    stype_import()

    print ' > Treatment'
    treat_import()

    print ' > Trays'
    trays_import()

    print '---------'
    print '>> Specimen Imports'
    print '> 2010 RT specimen import'
    rt2010_spec_import()
    
    print '> CW1 specimen import' 
    cw1_spec_import()

    print '> CW2 specimen import' 
    cw2_spec_import()

    print '> KIF11 specimen import'
    kif11_spec_import()

    print '> All KIF12 specimen import'
    kif12_spec_import()

    print '> BZ fish specimen import'
    bz_fish_spec(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/Zgliczynski_SampleIndex.csv')

    print '> 2011 PP specimen import'
    PP_2011_spec(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_PP_collections2.csv')

    print '> UVIC PP specimen import'
    Uvic_PP_import(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/UVICmacroprepping_sheet_data_WORKING_COPY_May24.csv')

    print '---------'    
    print '>> Start of Dissection Imports'
    print '> RT10 dissections'
    dis_import_RT10(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/RT_dissections10.csv')

    print '> CW1 dissections'
    dis_import_CW1(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/CW_merged_isotope_dissections2011.csv')

    print '> CW2 dissections'
    dis_import_CW2(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/CW_dis_merged_2012.csv')

    print '> KIF11 dissections'
    dis_import_KI11(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_fish_dissections.csv')

    print '> All KIF12 dissection import'
    dis_import_KI12(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/2012_Kiritimati_field_fish_dissections.csv')   

    print '---------'
    print '>> Start of Sample Imports'
    print '> KI sample index import'
    samp_import(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/KI_SI_sample_Index.csv')

    print '---------'
    print '>> Start of preprocessing imports'
    print '> SFU consolidated preprocessing'
    prep_import()

    print '> UVIC macro preprocessing import'
    uvic_prep_import()

    print '> BZ prep import'
    BZ_prep_import()

    print '> UVIC FISH prep import and sample creation'
    uvic_FISH_prep_import()

    print '> KI 2011 PP prep import and sample creation'
    ki_2011_pp_prep_import()
    

    print '---------'
    print'>> Shark data imports'
    print '> shark states'
    state_import()

    print '> shark pieces'
    piece_import()

    print '> shark specimens + hhs'
    shark_spec_import()

    print '> shark dissections'
    sharkdis_import()

    print '> shark samples import '
    shark_samp_prep_import()


    print '---------'
    print '>> Start of packing imports'
    
    print '> sfu packed import'
    sfu_packed_import()

    print '> UVIC 2011 packed import'
    uvic_2011_packed_import()
    
    print '> UVIC 2012 packed import'
    uvic_2012_packed_import()

    print '> species fishing methods and habitats'
    shmjoin_import()

    print '---------'
    print '>> Start of results imports'
    print '> SFU old results import'
    #results_import(filename = "/Users/jillian/Dropbox/Stable isotope database/input_data/SI Results/consolidated_sfu_results.csv")
    print '> UVic KI12TRAY1-7 import'
    results_import(filename = "/Users/jillian/Dropbox/Stable isotope database/input_data/SI Results/KIF_Tray1-7 data.csv")


    print ' > Specimen Spare Samples'
    spares_import()

    print '> Sample locations import'
    samp_locations(filename = '/Users/jillian/Dropbox/Stable isotope database/input_data/KI_SI_sample_Index.csv')


    print '---------'
    print ' > DONE!!!!!!!!!!'
    print '---------'

    #sys.exit("breather")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        f = sys.argv[1]
        if f in locals():
            print ' > running %s' % f
            try:
                filename = sys.argv[2]
                
            except:
                filename = None
            if filename:
                locals()[f](filename = filename)
            else:
                locals()[f]()
        else:
            print ' ERROR > %s not defined' % f
    else:
        main()
