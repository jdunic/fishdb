#!/usr/bin/python

import csv
from collections import Counter


f = csv.reader(open('sfu_packing_sheet_data_working_copy.csv','rb'))
writer = csv.writer(open('packing_duplicates.csv','wb'), dialect='excel')

from collections import Counter

samples=Counter()
for row in f:
    emails+=Counter([row[0]])

for row in f:
    if row[0] not in emails:
        writer.writerow(row)
        emails.add( row[0] )