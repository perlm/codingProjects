#! /usr/bin/env python

#Ideas for v2 - weeding out collaborating profs
#Weighting for early career v late.  Discount everything after first last-author occurence?

import urllib
import re
import sys

utils = "http://www.ncbi.nlm.nih.gov/entrez/eutils"
db     = "Pubmed"

round = 1
while round <= 5:
	esearch = utils + "/esearch.fcgi?" + "db=" + db + "&retmax=1&usehistory=y&term="
	if round == 1:
		query = raw_input("Author Name? Example: Smith AB\n")
		query  = query.rstrip('\r\n')		#Attempted chompp equivalent that may be unnecessary.
	else:
		query = advisor
	self = query
	words = []
	words =  query.split(" ")	#necessary since multi-line author list might separate first/last name

        esearch = esearch + query + "[AU]"
        esearch = esearch.replace(" ", "+")
        esearch_result = urllib.urlopen(esearch).read()
        Count = re.search( '(?<=<Count>)(.+)(?=</Count>)', esearch_result)
        Count = int(Count.group(0))
        QueryKey = re.search( '(?<=<QueryKey>)(.+)(?=</QueryKey>)', esearch_result)
        QueryKey = QueryKey.group(0)
        WebEnv = re.search( '(?<=<WebEnv>)(.+)(?=</WebEnv>)', esearch_result)
        WebEnv = WebEnv.group(0)

        if Count == 0:
                print "No papers!"
                sys.exit()

	efetch = utils + "/efetch.fcgi?" + "rettype=abstract&retmode=text&retstart=0&retmax=10000&db=" + db + "&query_key=" + QueryKey + "&WebEnv=" + WebEnv
	efetch_result = urllib.urlopen(efetch).read()


	#find authorship line and extract (at this point only last) authors.
	lines = []
	lines = efetch_result.split("\n\n")
	authors = []
	lasts = [];

	for line in lines:
		if words[0] in line:
			authors = line.split(",")
			for author in authors:
				check1 = author[:1]
				if check1 == " ":
					author = author[1:]
				check2 = author[-1:]
				if check2 == ".":
					author = author[:-1]
				last = author
			lasts.append(last)

#Using Last Authors, guess Advisor!
#In v1, just whoever shows up last most!

	votes = {}
	own = 0

	for name in lasts:
		if name == self:
			own += 1
		elif name in votes:
			votes[name] += 1
		else:
			votes[name] = 1

	max = 0
	for cans in votes.keys():
		if votes[cans] > max:
			max = votes[cans]
			advisor = cans

	number = Count - own
	print "Advisor =", advisor, "(Last author of", max, "of his/her", number, "non-last-author papers)"

	round += 1

