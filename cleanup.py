#!/usr/bin/env python
import csv

# CW 'master' merged sheet
csv1 = '/Users/jillian/Dropbox/Stable isotope database/input_data/CW_merged_isotope_dissections2011.csv'

csv2 = '/Users/jillian/Dropbox/Stable isotope database/input_data/CW_dis_merged_2012.csv'

master = list(csv.DictReader(open(csv1, 'rU')))
extra = list(csv.DictReader(open(csv2, 'rU')))
set1 = set(master)
set2 = set(extra)
print set1 - set2 # in 1, not in 2
print set2 - set1 # in 2, not in 1
print set1 & set2 # in both