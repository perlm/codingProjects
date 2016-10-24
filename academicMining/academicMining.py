#! /usr/bin/env python
import re,sys,time,os
import requests

termEntry = ['autism', 'asperger syndrome', 'obesity', 'vitamin', 'small pox', 'pus', 'corpuscle', 'bowel','Bilious', 'Canine madness', 'spleen','nano','micro','pico','femto','gout','polio','orangutan','natural','organic']

terms=[]
handles=[]
for t in xrange(len(termEntry)):
	if os.path.exists('data/%s.data' % (termEntry[t])):
		#name = terms.pop(t)
		print 'Already done: %s' % termEntry[t]
	else:
		terms.append(termEntry[t])

utils = "http://www.ncbi.nlm.nih.gov/entrez/eutils"
db     = "Pubmed"
esearch = utils + "/esearch.fcgi?" + "db=" + db + "&retmax=1&usehistory=y&term="

for t in xrange(len(terms)):
	handles.append(open('data/%s.data' % terms[t],'w'))
	print 'Running for: %s' % terms[t]
	for year in xrange(1930,2015):
		time.sleep(1)
	        searching = esearch + terms[t] + "[Title]" + "+AND+" + str(year) + "[Date+-+Publication]"
        	searching = searching.replace(" ", "+")
		Count = None
		while Count is None:
			try:
				search_result = requests.get(searching)
	        		Count = re.search( '(?<=<Count>)(.+)(?=</Count>)', search_result.text)
			except:
				print "Failed %s %s" % (year, terms[t])
				time.sleep(60)
				#pass

		try:
	        	Count = int(Count.group(0))
	                handles[t].write('%s\t%s\n' % (year,Count))
		except ValueError:
	                handles[t].write('%s\t0\n' % (year))

