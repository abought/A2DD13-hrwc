#! /usr/bin/env python

# Import python modules that will do useful stuff for us
import collections, csv

# code written for use by/for the Huron Valley Watershed Council (A2 DataDive 2013)
# Looks at the species table in the database, and outputs a file describing whether or not a given species is at a given site
# (value 0 = no, 1 = yes)
# Also prints out a list of the 10 surveys that showed the most species

# TODOS: 
# - Adapt GIS software to show these results on a map [GIS, d3]
#

# Code written and discussed by Nick Krabbenhoeft, @bernease/Bernease Herman; refactoring by Andy Boughton
# To use: output the database table for site surveys to comma-separated values (CSV) format; we based this analysis
# on the provided excel file "6- species list.csv"

## NOTES:
# final map likely ought to be spot-checked by ecologists/other workers or volunteers familiar with the data

#################

all_species = set()
all_surveys = {}
# First pass through the file: create a list of all known species in the database
with open('species.csv', 'rU') as f:
    reader = csv.reader(f)
    # skip header row
    reader.next()
    for row in reader:
    # Store species information in a dictionary whose key is the ID field in the database
    # (this may not be the same as the UniqueID field; as I understand it, this reports the most species-rich surveys, rather than 
    # the most species-rich bioreserves.  --abought

    # Convert species names to lowercase
    names_lowercase = [ item.lower() for item in row[5:] ]
        for item in names_lowercase:
        # Globally keep track of every unique species name listed. This list only combines obvious similarities (ELM and elm).
        # To detect more subtle similarities (Am. Elm vs American elm), the final output will need to be spot-checked by HRWC
            all_species.add( item )
    # Store species information in a dictionary based on the ID field (column 0) in the database
    # (this may not be the same as the UniqueID field, which we think is the name of the BioReserve). 
    # So the output of this file reports the most species-rich surveys, rather than 
    # the most species-rich bioreserves.  --abought
    all_surveys[ row[0] ] = collections.Counter( names_lowercase )
    #####
    # This next line is what connects a survey with an ID; change to row[1] to use the BioReserve ID instead of site ID
    all_surveys[ row[0] ]['survey_id'] = row[0]
    
    # We're not interested in blank columns, so get rid of those
    if '' in all_surveys[ row[0] ] : del all_surveys[ row[0] ]['']

all_species = sorted( all_species )
if '' in all_species: all_species.remove( '' )

# Wrte data to output file; first column should be the survey_id ("ID" = column 0 in database)
with open('survey_species2.tsv','w') as f:
    writer = csv.DictWriter( f, delimiter='\t', fieldnames=['survey_id'] + all_species , restval = 0 )
    writer.writeheader()
    for s in all_surveys:
        writer.writerow( all_surveys[s] )

# Lastly: can we find the 10 surveys/bioreserve sites that seem to have the most unique species?
rank_by_most_species = sorted( all_surveys , reverse = True, 
                key = lambda x: len( all_surveys[x].values() ) -1 )

print "Most species-rich surveys:"
print "Survey_id", "#species"
for i in range(10):
    survey_id = rank_by_most_species[i]
    print survey_id , len( all_surveys[ survey_id ].values() ) - 1

# Don't close the output window until the user is done looking at it
raw_input( "Analysis done! Press the return key to exit." )
