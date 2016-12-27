# -*- coding: utf-8 -*-

import glob, sys, string

# Do some really simple analysis!
# search for frequency of text terms

def read_summary():
	# read in summary file with title/author/year info
	summary	= {}
        with open('data/summary.txt','r') as f1:
                for line in f1:
                        cols				= line.split('\t')
			summary[(str(cols[0]),'title')]	= str(cols[1])
			summary[(str(cols[0]),'author')]= str(cols[2])
			summary[(str(cols[0]),'year')]	= str(cols[3]).rstrip()
	return summary

def read_texts():
	# read each text 
	book_texts = {}
	for f in glob.glob("data/[0-9]*.txt"):
		book_id = f[5:-4]
		print f, book_id
		with open(f, 'r') as f1:
			book_texts[book_id] = f1.read()
	return book_texts
		

def search_for_wisdom(book_texts,summary,search='wisdom'):
	# book_texts is a dictionary keyed on bookid
	# summary is a dict keyed on a tuple with bookid
	# count frequency of a particular word (use "wisdom" here)
	# plot in R.
	# not that interesting.

        f1 = open('analysis/%s.data' % search,'w')

	for book in book_texts:

		# NEED TO REMOVE PUNCTUATION
		book_text = book_texts[book].translate(None, string.punctuation)
		words = book_text.split()
		book_length = len(words)
		words = map(lambda x:x.lower(),words)
		search_count = words.count(search)
		search_rate = float(search_count)/book_length
	
		title = summary[(book,'title')]
		author = summary[(book,'author')]
		year = summary[(book,'year')]
		f1.write('{},{},{},{},{}\n'.format(book,title.replace(',',''),author.replace(',',''),year,search_rate))


if __name__ == "__main__":
	
	summary = read_summary()
	book_texts = read_texts()
	search_for_wisdom(book_texts,summary)
