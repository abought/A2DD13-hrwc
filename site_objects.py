## README in-comments:
# this script separates sites into objects 
# s.t. another script can apply the correct info to a map easily

# due to the double-meaning of commas in the survey_species.csv file, 
# script was altered to \t separation to produce a .tsv file, included in the repo,
# which was used here.

# current __str__ representation serves to represent the information gathered in each object
# + for testing


# TODO: refactor


import csv


class HVWC_Site(object):
	def __init__(self, rowlist):
		with open('survey_species.tsv', 'rU', ) as f: # this is terrible style, yes
			reader = csv.reader(f, delimiter='\t')
			headings = list(reader)[0]

		self.id = rowlist[0]
		self.num_species = len([x for x in rowlist if x == '1'])
		self.species = sorted([x[0] for x in zip(headings, rowlist) if x[1] == '1'])

		if len(self.species) != self.num_species:
			print "ERROR: something is wrong with filename or implementation"


	def __str__(self):
		s = "SITE ID: %s \n %d species at site \n" % (self.id, self.num_species)
		if self.num_species > 0:
			s += "\n first alphabetical species name: %s" % self.species[0]
		return s




if __name__ == '__main__':

	site_objects = []

	with open('survey_species.tsv', 'rU') as fnew:
		rnew = csv.reader(fnew, delimiter='\t')
		ls = list(rnew)[1:] # list of lists, not including headings
		for site in ls: # each site is a list
			site_objects.append(HVWC_Site(site))
 
		for item in site_objects[:25]: # testing
			print item




