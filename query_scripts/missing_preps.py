#!/usr/bin/env python

import os
from django.core.management import setup_environ
from fishdb import settings
setup_environ(settings)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fishdb.settings")
from django.db import models
from fishdb.models import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# random python libraries:
import sys
import csv
from datetime import datetime


samples = Samples.objects.select_related().all()

for s in samples:

    try:
        sample = s.SampleID
        treatment = s.preprocessings_set.get().fk_Treatment.TreatmentCode

    except ObjectDoesNotExist as e:
        logging.warn('sample %s %s' % (sample, e))

















