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
from subprocess import call
from django.core.management import setup_environ

from fishdb import settings
from datetime import datetime
from decimal import Decimal
import sys

setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")

import csv
import collections
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

#from django.core.management import setup_environ
from fishdb.models import *

import logging
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
            fmp_habitatID = row['pk_FishingHabitatID']
            habitat = row['FishingHabitat']

            habs, created = FishingHabitats.objects.get_or_create(
                fmp_habitat = fmp_habitatID,
                Habitat = habitat
            )

            if created:
                habs.save()

def fm_import():    
    filename = 'csv_data/FishingMethods.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
                fmp_methodID = row['pk_FishingMethodID']
                method = row['FishingMethod']

                meths, created = FishingMethods.objects.get_or_create(
                    fmp_methodID = fmp_methodID,
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
    filename = 'csv_data/LengthWeights.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            date = row['DateUpdated']
            fb_maxL = row['FishBaseMaxLength']
            fb_maxRef = row['FishbaseMaxLengthRef']
            fb_Ltype = row['FishbaseMaxLengthType']
            LtoMeas = row['LengthToMeasure']
            locale = row['Locale']
            modelSp = row['ModelSpecies']
            notes = row['Notes']
            parA = row['ParameterA']
            parB = row['ParameterB']
            fmp_LWid = row['pk_LengthWeightID']
            source = row['Sources']
            spp = row['SpeciesCode']

        # Putting date in datetime format:
            dated = datetime.strptime(date, '%Y-%m-%d').date()

        # Putting number strings into decimals (and watching out for NULLS!!!!):
            
            if fb_maxL == '':
                fb_L = None
            else:
                fb_L = Decimal(fb_maxL)
            
            if parA == '':
                A = None
            else: 
                A = Decimal(parA)
            
            if parB == '':
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
                Locale = locale,
                fmp_LWid = fmp_LWid
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

def sp_import():
    filename = 'csv_data/Taxonomies.csv'
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
                if created:
                    logging.info('created lengthweights: %s' % lw)
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
                Notes=notes,
                fmp_pk=fmp_siteID
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
                fmp_pk=pk_SampleTypeID
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

def shjoin_import():
    filename = 'csv_data/Species_Habitat_Joins.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            fk_FishingHabitat = row['fk_FishingHabitatID']
            fk_SpeciesID = row['fk_SpeciesID']

            # FK lookups:
            hab = FishingHabitats.objects.get(fmp_habitat=fk_FishingHabitat)
            
            try:
                spp = Species.objects.get(fmp_pk=fk_SpeciesID)
                # assigning values:
                spp.Habitat.add(hab)
                spp.save()
            except ObjectDoesNotExist as e:
                logging.warn('spp %s does not exist' % fk_SpeciesID)

def smjoin_import():
    filename = 'csv_data/Species_Method_Joins.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            fk_FishingMethodID = row['fk_FishingMethodID']
            fk_SpeciesID = row['fk_SpeciesID']

            # FK lookups:
            try:
                meth = FishingMethods.objects.get(fmp_methodID=fk_FishingMethodID)
                spp = Species.objects.get(fmp_pk=fk_SpeciesID)
                # assigning values:
                spp.Methods.add(meth)
                spp.save()
            except ObjectDoesNotExist as e:
                logging.warn('spp %s dne' % fk_SpeciesID)

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
                    print spp
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
                logging.warn('%s:%s %s' % (filename, line_number, e))

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
                logging.error(" line: %s:%s is not unique" %
                    (line_number, SpecimenID
                ))

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

def PP_2011_spec(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_PP_collections.csv'):
    
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

            DateDissected = row['DateDissected']
            DissectedBy = row['DissectedBy']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            gh = row['gh']
            gw = row['gw']
            wt = row['wt']
            notes = row['notes']
            oto = row['OtolithSample']
            PreySize = row['PreySizeInStomach']
            StomachContents = row['StomachContents']



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
            if DateDissected == '': DateDissected = None
            elif DateDissected == 'NA': DateDissected = None

            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    gh=gh,
                    gw=gw,
                    DateDissected=DateDissected,
                    StomachContents=StomachContents,
                    PreySize=PreySize,
                    OtolithSample=oto,
                    DissectedBy=DissectedBy,
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
                pass
                #logging.error("%s Exception: %s" % (line_number, e))

            DateDissected = row['DateDissected']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            wt = row['wt']
            gh = row['gh']
            gw = row['gw']
            Notes = row['Notes']
            StomachContents = row['StomachContents']
            PreySize = row['PreySize']
            oto = row['oto.sample']
            PhotoName = row['photo']
            iso = row['iso.sample']
            DissectedBy = row['DissectedBy']

            DateDissected = shitty_date_conversion(DateDissected, blank=True)

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

            if DateDissected == '': DateDissected = None
            elif DateDissected == 'NA': DateDissected = None

            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    gh=gh,
                    gw=gw,
                    PreySize=PreySize,
                    OtolithSample=oto,
                    PhotoName=PhotoName,
                    IsotopeSample=iso,
                    DateDissected=DateDissected,
                    StomachContents=StomachContents,
                    Notes=Notes,
                    DissectedBy=DissectedBy
                )

                if created:
                    dis.save()
            except Exception as e:
                logging.error("%s:%s %s" % (filename, line_number, e))


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
                pass
                #logging.error("%s Exception: %s" % (line_number, e))

            DateDissected = row['DateProcessed']
            tl = row['TL']
            fl = row['FL']
            sl = row['SL']
            wt = row['wt']
            gh = row['gh']
            gw = row['gw']
            Notes = row['notes']
            StomachContents = row['StomachContents']
            PreySize = row['PreySize']
            oto = row['otoliths']
            iso = row['iso.sample']
            DissectedBy = row['DissectedBy']
            spp = row['species']
            StomachSample = row['stom.sample']

            DateDissected = shitty_date_conversion(DateDissected, blank=True)

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
                Notes += ". Original recorded weight: %s" % wt
                wt_num = wt.translate(None, 'lbs')
                wt = float(wt_num)*454
            
            #    try:
             #       tl = float(tl)*25.4
              #      fl = float(fl)*25.4
               #     sl = float(sl)*25.4
                #except TypeError as e:
                 #   print '%s %s' % (line_number, e)

            if DateDissected == '': DateDissected = None
            elif DateDissected == 'NA': DateDissected = None

            if StomachSample == 'N':
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
                        PreySize=PreySize,
                        OtolithSample=oto,
                        IsotopeSample=iso,
                        DateDissected=DateDissected,
                        StomachContents=StomachContents,
                        Notes=Notes,
                        DissectedBy=DissectedBy
                    )

                    if created:
                        dis.save()
                except Exception as e:
                    logging.error("%s:%s %s" % (filename, line_number, e))

"""def spec_import():
    filename = 'csv_data/Specimens.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 0
        for row in csvreader:
            line_number += 1
            CollectedBy = row['CollectedBy']
            CollectionNotes = row['Collection Notes']
            CollectionMethod = row['CollectionMethod']
            DateCollected = row['DateCollected']
            DateEntered = row['DateEntered']
            DepthCollected = row['DepthCollected']
            fmp_siteID = row['fk_SiteID']
            fmp_speciesID = row['fk_SpeciesID']
            OldID1 = row['OldID1']
            fmp_specimenID = row['pk_SpecimenID']
            sex = row['Sex']
            SpecimenID = row['SpecimenID']

            # FK lookups:
            if fmp_siteID == '':
                fmp_siteID = 42

            try:
                site = Sites.objects.get(fmp_pk=fmp_siteID)
                spp = Species.objects.get(fmp_pk=fmp_speciesID)
            except Exception as e:
                logging.warn('%s:%s %s' % (filename, line_number, e))


            try:
                meth = CollectionMethods.objects.get(Method=CollectionMethod)
            except:
                meth = None

            if DateCollected == '': DateCollected = None

            # assigning values:
            try:
                spe, created = Specimens.objects.get_or_create(
                    fk_Site=site,
                    fk_Species=spp,
                    fk_Method=meth,
                    SpecimenID=SpecimenID,
                    CollectedBy=CollectedBy,
                    Sex=sex,
                    OldID1=OldID1,
                    DateEntered=DateEntered,
                    CollectionNotes=CollectionNotes,
                    DateCollected=DateCollected,
                    DepthCollected=DepthCollected,
                    fmp_pk=fmp_specimenID
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
"""

"""def dis_import(filename = 'csv_data/Dissections.csv'):
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        line_number = 0
        for row in csvreader:
            line_number += 1
            fmp_specimen_id = row['fk_SpecimenID']
            # get specimen here

            try:
                specimen = Specimens.objects.get(fmp_pk=fmp_specimen_id)
            except Exception as e:
                logging.error("%s:%s Exception: %s" % (
                    filename, line_number, e
                ))

            DateDissected = row['DateDissected']
            DateEntered = row['DateEntered']
            DissectedBy = row['DissectedBy']
            fl = row['FLMM']
            gh = row['gh']
            gonads = row['GonadsRipe']
            gw = row['gw']
            isotope = row['IsotopeSample']
            notes = row['Notes']
            oto = row['OtolithSample']
            photo = row['PhotoFileName']
            PreySize = row['PreySizeInStomach']
            sl = row['SLMM']
            stomach_contents = row['StomachContents']
            stomach_sample = row['StomachSample']
            tl = row['TLMM']
            wt = row['wt']

            if fl == '': fl = None
            if gh == '': gh = None
            if gw == '': gw = None
            if sl == '': sl = None
            if tl == '': tl = None
            if wt == '': wt = None
            if DateDissected == '': DateDissected = None
            elif DateDissected == 'NA': DateDissected = None

            try:
                dis, created = Dissections.objects.get_or_create(
                    fk_Specimen = specimen,
                    TL=tl,
                    FL=fl,
                    SL=sl,
                    wt=wt,
                    gh=gh,
                    gw=gw,
                    DateDissected=DateDissected,
                    DateEntered=DateEntered,
                    StomachContents=stomach_contents,
                    PreySize=PreySize,
                    StomachSample=stomach_sample,
                    IsotopeSample=isotope,
                    OtolithSample=oto,
                    GonadsRipe=gonads,
                    PhotoName=photo,
                    DissectedBy=DissectedBy,
                    Notes=notes
                )

                if created:
                    dis.save()
            except Exception as e:
                logging.error("%s:%s %s" % (filename, line_number, e))
"""

def samp_import():
    filename = 'csv_data/Samples.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            fmp_specimenID = row['fk_SpecimenID']
            notes = row['notes']
            fmp_pk_samp = row['pk_SampleID']
            ref_type = row['ref_type']
            SampleID = row['SampleID']

        # FK lookup:
            specimen = Specimens.objects.get_or_create(fmp_pk=fmp_specimenID)
            stype = SampleTypes.objects.get_or_create(SampleType=ref_type)

        # assigning values:
            samp, created = Samples.objects.get_or_create(
                fk_Specimen=specimen,
                fk_SampleType=stype,
                SampleID=SampleID,
                Notes=notes,
                fmp_pk=fmp_pk_samp
            )

            if created:
                samp.save()

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

def sharkdis_import():
    filename = 'csv_data/SharkDissections.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            DorsalBase = row['DorsalBase']
            DorsalHeight = row['DorsalHeight']
            fmp_specimenID = row['fk_SpecimenID']
            ForkLength = row['ForkLength']
            notes = row['Notes']
            PectoralBase = row['PectoralBase']
            PectoralHeight = row['PectoralHeight']
            photo = row['PhotoTaken']
            PCL = row['PrecaudLength']
            stretch = row['StretchLength']
            TailBase = row['TailBase']
            TailHeight = row['TailHeight']
            TL = row['TL']
            wt = row['Weight_lbs']
            date = row['DateDissected']

        # Fk lookups:
            specimen = Specimens.objects.get_or_create(fmp_pk=fmp_specimenID)

            sds, created = SharkDissections.objects.get_or_create(
                fk_Specimen=specimen,
                PCL=PCL,
                FL=ForkLength,
                TL=TL,
                stretch=stretch,
                DH=DorsalHeight,
                DB=DorsalBase,
                PH=PectoralHeight,
                PB=PectoralBase,
                TH=TailHeight,
                TB=TailBase,
                wt=wt,
                PhotoTaken=photo,
                Notes=notes,
                DateDissected=date
            )

            if created:
                sds.save()

def sharksamp_import():
    filename = 'csv_data/SharkSamples.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            DateDissected = row['DateDissected']
            notes = row['Notes']
            fmp_hhsID = row['fk_hhsID']
            ref_sampleID = row['ref_SampleID']
            ref_piece = row['ref_sharkpiece']
            ref_state = row['ref_sharkstate']

        # FK lookups:
            hhs = HHS.objects.get_or_create(fmp_pk=fmp_hhsID)
            samp = Samples.objects.get_or_create(Sample=ref_sampleID)
            piece = SharkPieces.objects.get_or_create(SharkPiece=ref_piece)
            state = SharkStates.objects.get_or_create(State=ref_state)

            ss, created = SharkSamples.objects.get_or_create(
                fk_Sample=samp,
                fk_SharkPiece=piece,
                fk_State=state,
                fk_HHS=hhs
            )

            if created:
                ss.save()

def prep_import():
    filename = 'csv_data/Preprocessings.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            DateGround = row['DateGround']
            DateWashed = row['DateWashedDried']
            DryingHours = row['DryingHours']
            method = row['DryingMethod']
            notes = row['Notes']
            fmp_preprocessings = row['pk_PreprocessingID']
            PrepEnteredBy = row['PrepEnteredBy']
            PreppedBy = row['PreppedBy']
            samp = row['ref_SampleID']
            treat = row['ref_treatment']
        
        # FK lookups:
            sample = Samples.objects.get_or_create(SampleID=samp)
            treatment = Treatments.objects.get_or_create(Treatment=treat)

        # assigning values:
            prep, created = Preprocessings.objects.get_or_create(
                fk_Sample=sample,
                fk_Treatment=treatment,
                DateWashDry=DateWashed,
                PreppedBy=PreppedBy,
                PrepEntered=PrepEnteredBy,
                DateGround=DateGround,
                DryingMethod=method,
                DryingTime=DryingHours,
                Notes=notes,
                fmp_preprocessings=fmp_preprocessings
            )

            if created:
                prep.save()

def packed_import():
    filename = 'csv_data/PackedSamples.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            capwt = row['CapsuleWeight']
            DateEntered = row['DateEntered']
            EnteredBy = row['EnteredBy']
            DatePacked = row['DatePacked']
            FilledCapsuleWeight = row['FilledCapsuleWeight']
            notes = row['Notes']
            PackedBy = row['PackedBy']

            sampleID = row['ref_sampleID']
            trayID = row['ref_TrayName']
            wt = row['SampleWeight']
            tcol = row['TrayColumn']
            trow = row['TrayRow']

            fmp_packedID = row['pk_PackedID']
        # FK lookups:
            sample = Samples.objects.get_or_create(SampleID=sampleID)
            tray = Trays.objects.get_or_create(TrayName=TrayName)
        # importing data into table:
            ps, created = PackedSamples.objects.get_or_create(
                fk_Sample = sample,
                fk_TrayName = tray,
                TrayRow = trow,
                TrayColumn = tcol,
                CapWeight = capwt,
                FilledCapWeight = FilledCapsuleWeight,
                SampleWeight = wt,
                PackedBy = PackedBy,
                EnteredBy = EnteredBy,
                DatePacked = DatePacked,
                DateEntered = DateEntered,
                Notes = notes,
                fmp_packedID = fmp_packedID
            )

            if created:
                ps.save()

def result_import():
    filename = 'csv_data/Results.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            d13C = row['d13C']
            d15N = row['d15N']
            DateProcessed = row['DateProcessed']
            Lab = row['Lab']
            fmp_packedID = row['fk_PackedID']
        
        # FK lookups:
            packed = PackedSamples.objects.get_or_create(fmp_packedID=fmp_packedID)

        # assigning values:
            results, created = Results.objects.get_or_create(
                fk_Packed=packed,
                d13C=d13C,
                d15N=d15N,
                Lab=Lab,
                DateProcessed=DateProcessed
            )

            if created:
                results.save()      

def samp_loc_import():
    filename = 'csv_data/SampleLocations.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            DateStatus = row['DateStatusUpdated']
            EnteredBy = row['EnteredBy']
            fmp_location = row['fk_LocationID']
            fmp_sampleID = row['fk_sampleID']
            inst = row['Institution']
            number = row['ref_containNum']
            container = row['ref_containType']

        # FK lookup:
            sample = Samples.objects.get_or_create(fmp_sampleID=fmp_pk)
            loc = Locations.objects.get_or_create(fmp_locationID=fmp_location)

        # assigning values:
            sl, created = SampleLocations.objets.get_or_create(
                fk_Sample=sample,
                fk_Location=loc,
                DateUpdated=DateStatus,
                EnteredBy=EnteredBy,
                Institution=inst
            )

            if created:
                sl.save()

def sss_import():
    filename = 'csv_data/SpecimenSpareSamples.csv'
    with open(filename, 'rU') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            cont = row['Container']
            inst = row['Institution']
            specimenID = row['ref_SpecimenID']

        # FK lookups:
            spec = Specimens.objects.get_or_create(SpecimenID=specimenID)

        # assigning values:
            sss, created = SpecimenSpareSamples.objects.get_or_create(
                fk_Specimen=spec,
                Container=cont,
                Institution=inst,
            )

            if created:
                sss.save()

# dirty dirty dirty
def main():
    db = os.path.join(os.getcwd(), "db/sqlite3.db")
    call(["rm %s" % db], shell=True)
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

    print ' > SpeciesTypes'
    sp_type()

    print ' > Species'
    sp_import()

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

    print ' > Species-Habitat'
    shjoin_import()

    print ' > Species-Methods'
    smjoin_import()


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

    print '> 2011 PP spec import'
    PP_2011_spec(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_PP_collections.csv')
    
    print '>> Start of Dissection Imports'
    print '> RT10 dissections'
    dis_import_RT10(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/RT_dissections10.csv')

    print '> CW1 dissections'
    dis_import_CW1(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/CW_merged_isotope_dissections2011.csv')

    print '> CW2 dissections'
    dis_import_CW2(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/CW_dis_merged_2012.csv')

    print '> KIF11 dissections'
    dis_import_KI11(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2011_KI_fish_dissections.csv')

    print '> All KIF12 dissection import'
    dis_import_KI12(filename='/Users/jillian/Dropbox/Stable isotope database/input_data/2012_Kiritimati_field_fish_dissections.csv')    

    sys.exit("breather")
    
    print ' > Specimens'
    spec_import()

    print ' > Dissections'
    dis_import()

    print ' > Samples'
    samp_import()

    print ' > State'
    state_import()

    print ' > Shark Pieces'
    piece_import()

    print ' > Shark Dissections'
    sharkdis_import()

    print ' > Shark Samples'
    sharksamp_import()

    print ' > Preprocessings'
    prep_import()

    print ' > Packed Samples'
    packed_import()

    print ' > Results'
    result_import()

    print ' > Sample Locations'
    samp_loc_import()

    print ' > Specimen Spare Samples'
    sss_import()

    print ' > DONE!!!!!!!!!!'

if __name__ == "__main__":
    main()
