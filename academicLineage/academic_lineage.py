#! /usr/bin/env python

#Ideas for v2 - Weighting for early career v late.  Discount everything after first last-author occurence?

import urllib,re,sys
from collections import Counter

def main(name):
	utils = "http://www.ncbi.nlm.nih.gov/entrez/eutils"
	db     = "Pubmed"

	advisor_dict = {}
	round = 1
	while round <= 3:
		esearch = utils + "/esearch.fcgi?" + "db=" + db + "&retmax=1&usehistory=y&term="
		if round == 1:
			query  = name
		else:
			query = advisor
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
			break

		efetch = utils + "/efetch.fcgi?" + "rettype=abstract&retmode=text&retstart=0&retmax=10000&db=" + db + "&query_key=" + QueryKey + "&WebEnv=" + WebEnv
		efetch_result = urllib.urlopen(efetch).read()

		#find authorship line and extract (at this point only last) authors.
		# authorship can be on more than one line.
		lineNumbers = []
		lines = efetch_result.split("\n\n")
		for n,line in enumerate(lines):
			if 'Author information' in line:
				lineNumbers.append(n)
		
		lasts = []
		for n in lineNumbers:
			n = n -1
			line = lines[n]
			authors = line.split(",")
			if words[0] not in authors[-1]:
				lasts.append(authors[-1].strip())
			else:
				try:
					lasts.append(authors[-2].strip())
				except:
					pass
		lasts2 = map(lambda each:re.sub("[.()1234567890]","",each), lasts)

		#Using Last Authors, guess Advisor!
		#In v1, just whoever shows up last most!
		if len(lasts2)==0:
			break
		votes = Counter(lasts2)
		advisor = max(votes,key=votes.get)

		number = votes[advisor]
		advisor_dict[advisor] = number
		#print "Advisor =", advisor, "(Last author on ", number, " papers)"

		round += 1
	return advisor_dict

if __name__ == "__main__":
	query = raw_input("Author Name? Example: Smith AB\n")
	query  = query.rstrip('\r\n')
        advisor_dict = main(query)
	print advisor_dict

