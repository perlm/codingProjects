#!/usr/bin/python

##################################################
# solve a puzzle!
# http://fivethirtyeight.com/features/this-challenge-will-boggle-your-mind/
##################################################

import random, re

#recursion
def find_more_words(w, words,store=None):
	if store is None:store=[]
	for w2 in words:
		if re.match(r'{0}[a-z]$'.format(w),w2):
			print w2
			store.append(w2)
			find_more_words(w2,words,store)
	return store


def express(start=2):
	with open('/usr/share/dict/words') as f:
		    words = f.read().splitlines()
	words = map(lambda x:x.lower(),words)
	longestWord= max(words, key=len)
	maxLength = len(longestWord)

	# can't trust this- since it lists every letter is a word.
	if start==1:
		startList = ['a','i']
	else:
		startList = [w for w in words if len(w)==start]

	stored =[]
	for w in startList:
		stored += find_more_words(w,words)
	
	stored2 = list(set(stored))
	stored2.sort(key = len, reverse=True)
	print stored2

	outfile = open('riddler_20161021.dat', 'w')
	outfile.write("\n".join(stored2))



if __name__ == '__main__':
	express(start=2)
	# next steps- try starting with all 2 letter words, instead of just a,i.
	# apply scrabble limitations!

	

