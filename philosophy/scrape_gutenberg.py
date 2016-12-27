# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, SoupStrainer
import requests, re,sys,os, time

# The goal of this project is to do text analysis on works of philosophy.

# project gutenberg has lots
# I'll try starting with gutenberg's list of philosophy books, downloading and cleaning them.
# I used bits of this code as a guide - https://github.com/ropenscilabs/gutenbergr


def get_ebook_ids(start):
	# start with Gutenberg's philosophy bookshelf 
	# return ebook id numbers

	# this page links to pages that are intermediary. easier to just grab the id numbers
	ids = []
        #r = requests.get(start)
	r = sleeper(start)
	soup = BeautifulSoup(r.text, 'html.parser')
	for link in soup.find_all('a'):
		if link.get('href') is not None and 'ebook' in link.get('href'):
			#print link
			#print link.get('title')
			idmatch = re.match(r'ebook:([0-9]+)', link.get('title'))
			try:
				ids.append(idmatch.group(1))
				#print idmatch.group(1)
			except AttributeError:pass
	return ids


def download_list(ids):
	# given a list of ids to download - check to see if it exists and if it does not then download it.

	f1 = open('data/summary.txt','a+')

	for iii in ids:

		# skip inconsistently formatted for now
		if iii in ['4391','690']:continue

		newfile = 'data/{}.txt'.format(iii)
		if not os.path.isfile(newfile):

			ebook = download(iii)
			if check_download(ebook):continue

			title, author, year, text = process_text(ebook)
	
			f2 = open(newfile,'w')
			f2.write('{}'.format(text))

			f1.write('{}\t{}\t{}\t{}\n'.format(iii,title,author,year))
		#sys.exit()

def check_download(ebook):
	# check if this doesn't exist and skip for now.
	if '<title>404 Not Found</title>' in ebook:
		return True
	else:
		return False


def sleeper(url):
	while True:
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		if soup.find("div", {"id": "recaptcha_widget"}) is None:
			time.sleep(1)
			return r
		#print soup
		print 'captcha\'d on {}'.format(url)
		sys.exit('captcha\'d on {}'.format(url))
		time.sleep(300)


def download(ebook_id):
	# download and quickly parse out book info
	# apparently there are two different possible url's? 
	# switch to just the mirror url

	#url = 'http://www.gutenberg.org/cache/epub/{i}/pg{i}.txt'.format(i=ebook_id)
	#url = 'http://www.gutenberg.org/files/{i}/{i}.txt'.format(i=ebook_id)
	a = '/'.join([ebook_id[i] for i in xrange(len(ebook_id)-1)])
	url = 'http://www.gutenberg.lib.md.us/{a}/{i}/{i}.txt'.format(a=a,i=ebook_id)
	r = sleeper(url)
	ebook =  r.text.encode('utf-8').replace('\r','')
	print "DOWNLOADING", ebook_id
	#print ebook
	return ebook

		

def process_text(ebook):
	# ebook is text from ebook
	titlematch = re.search(r'Title: (.+)\n', ebook)
	try:
		title = titlematch.group(1)
		print 'title = ', title
	except:
		print "NO TITLE", ebook

	authormatch = re.search(r'Author: (.+)\n', ebook)
	try:
		author = authormatch.group(1)
		print 'author = ', author
	except:
		print "NO AUTHOR", ebook
	
	# looks like the first date after "start" is most often the write one.
	# though definitely not very reliable - I went in by hand to fix a bunch
	yearmatch = re.search(r'START OF (THIS|THE) PROJECT GUTENBERG EBOOK.+?(1[0-9][0-9][0-9])', ebook,re.M|re.S)
	try:
		year = yearmatch.group(2)
	except:
		year = ''

	# remove some header and tailer
	# need re.M|re.S for multiline
	textmatch = re.search(r'START OF (THIS|THE) PROJECT GUTENBERG EBOOK.+?\n(.+?)END OF (THIS|THE) PROJECT GUTENBERG EBOOK',ebook,  re.M|re.S)
	try:
		text = textmatch.group(2)
	except:
		print "NO TEXT", ebook

	assert 3<=len(title)<=500 and 3<=len(author)<=50 and 100<=len(text)<=10000000, 'download fail! {} {} {}'.format(title, author,len(text))

	return title, author, year, text


if __name__ == "__main__":
	start = 'http://www.gutenberg.org/wiki/Philosophy_(Bookshelf)'
	ids = get_ebook_ids(start)
	download_list(ids)

