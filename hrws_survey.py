# code written and discussed by @nickkrabbenhoeft, @bernease
# refactoring intended

# TODO: refactor!

# code for the Huron Valley Watershed Council 
# separate out species list
# intended for creation of interactive map
# TODO: map [GIS, d3]

from __future__ import print_function
import csv

all_species = set()
all_species_sort = []

survey_dict = {}
species_key = {}

with open('species.csv', 'rU') as f:
    reader = csv.reader(f)
    i=0
    for row in reader:
    	if i==0:
    		i=1
    		continue
    	survey_dict[row[0]] = [0 for i in range(1478)]
        row = row[5:]
        for item in row:
        	all_species.add(item.lower()) # s.t. no duplicates due to manual-entry capitalization issues
            # (intended for interactive map, thus capitalization not explicitly necessary at this juncture)


for item in all_species:
	all_species_sort.append(item)

all_species_sort = sorted(all_species)
all_species_sort = all_species_sort[1:]

j=0
for item in all_species_sort:
	species_key[item] = j
	j += 1

with open('species.csv', 'rU') as f:
    reader = csv.reader(f)
    i=0
    for row in reader:
    	if i==0:
    		i=1
    		continue
    	key = row[1] # bioreserve id
    	row = row[5:]
    	for item in row:
    		if item!='':
    			survey_dict[key][species_key[item]] = 1

f = open('survey_species.csv','wb')
f.write('id')
for item in all_species_sort:
	f.write(',')
	f.write(item)
f.write('\n')
for item in survey_dict:
	f.write(item)
	for listitem in survey_dict[item]:
		f.write(',')
		f.write(str(listitem))
	f.write('\n')

f.close()