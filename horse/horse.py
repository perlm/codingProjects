#!/usr/bin/python

##################################################
# play horse
##################################################

import random

def horse(pa, pb):

	# pa and pb are their preferred shot prob's
	# assume they are equally capable players, who shoot the same when matching.
	pa2 = pb
	pb2 = pa
	(lettersA , lettersB) = 0,0
	made = 0

	rounds = 0

	while True:
		rounds += 1
		# player A's turn
		if made==1:
			if (random.random()>pa2):
				lettersA += 1
				#print "A misses ", "horse"[0:lettersA] 
				if lettersA == 5:
					return ("B", rounds)
			#else:print "A matches"
			made = 0
		else:
			if (random.random()<pa):
				made = 1
				#print "A makes"
			else:
				made = 0
				#print "A misses"

		# player B's turn
		if made==1:
			if (random.random()>pb2):
				lettersB += 1
				#print "B misses ", "horse"[0:lettersB] 
				if lettersB == 5:
					return ("A",rounds)
			#else:print "B matches"
			made = 0
		else:
			if (random.random()<pb):
				made = 1
				#print "B makes"
			else:
				made = 0
				#print "B misses"


if __name__ == '__main__':

	#w= horse(0.95,0.5)
	f1 = open('results2.log','w')

	iters = 10000
	for x in [x * 0.01 for x in range(1, 100)]:
		a = 0
		rAvg = 0
		for i in xrange(iters):
			#(w,r)= horse(x,0.5)
			(w,r)= horse(0.5,x)
			if w=='A':
				a+=1
			rAvg += r
		f1.write('%s\t%s\t%s\n' % (x, float(a)/iters, float(rAvg)/iters))



