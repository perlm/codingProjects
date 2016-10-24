#!/usr/bin/env python

import random

def simulateGvB(fracThrees):
	f1 = open('data1','w')
	#Good vs Bad
	attempts = 83		#median 2014-15 season
	fgThreeA = 0.4		#near best
	fgThreeB = 0.3		#near worst
	fgTwoA = 0.5		#near best
	fgTwoB = 0.45		#near best
	winner=[]
	for x in xrange(0,100000):
		scoreA=0
		scoreB=0
		for p in xrange(attempts):
			if random.random()<fracThrees:
				if (random.random()<fgThreeA):scoreA+=3
			else:
				if (random.random()<fgTwoA):scoreA+=2

			if random.random()<fracThrees:
				if (random.random()<fgThreeB):scoreB+=3
			else:
				if (random.random()<fgTwoB):scoreB+=2
		diff = scoreA-scoreB
		f1.write('%s\t%s\n' % (fracThrees,diff))
		if scoreA>scoreB:winner.append(0)
		elif scoreA<scoreB:winner.append(1)
		else:winner.append(0.5)
		
	upsetFreq = sum(winner)/float(len(winner))
	return upsetFreq

def simulateGoodvsAve(fracThrees):
	#Good vs Ave
	attempts = 83		#median 2014-15 season
	fgThreeA = 0.4		#near best
	fgThreeB = 0.35		#ave
	fgTwoA = 0.5		#near best
	fgTwoB = 0.475		#ave
	winner=[]
	for x in xrange(0,100000):
		scoreA=0
		scoreB=0
		for p in xrange(attempts):
			if random.random()<fracThrees:
				if (random.random()<fgThreeA):scoreA+=3
			else:
				if (random.random()<fgTwoA):scoreA+=2

			if random.random()<fracThrees:
				if (random.random()<fgThreeB):scoreB+=3
			else:
				if (random.random()<fgTwoB):scoreB+=2
		if scoreA>scoreB:winner.append(0)
                elif scoreA<scoreB:winner.append(1)
                else:winner.append(0.5)
		
	upsetFreq = sum(winner)/float(len(winner))
	return upsetFreq

def simulateTwovsThree(fracThrees):
	#Good 2pt vs Good 3pt
	attempts = 83		#median 2014-15 season
	fgThreeA = 0.3		#worst
	fgThreeB = 0.4		#best
	fgTwoA = 0.5		#best
	fgTwoB = 0.45		#worst
	winner=[]
	for x in xrange(0,100000):
		scoreA=0
		scoreB=0
		for p in xrange(attempts):
			if random.random()<fracThrees:
				if (random.random()<fgThreeA):scoreA+=3
			else:
				if (random.random()<fgTwoA):scoreA+=2

			if random.random()<fracThrees:
				if (random.random()<fgThreeB):scoreB+=3
			else:
				if (random.random()<fgTwoB):scoreB+=2
		if scoreA>scoreB:winner.append(0)
                elif scoreA<scoreB:winner.append(1)
                else:winner.append(0.5)
		
	upsetFreq = sum(winner)/float(len(winner))
	return upsetFreq

def simulateAvevsAve(fracThrees):
	#change freq of 3 attempts for only 1 team
	f2 = open('data2','w')
	attempts = 83		#median 2014-15 season
	fgThreeA = 0.3333
	fgThreeB = 0.3333
	fgTwoA = 0.5
	fgTwoB = 0.5
	winner=[]
	for x in xrange(0,100000):
		scoreA=0
		scoreB=0
		for p in xrange(attempts):
			if random.random()<0.0:
				if (random.random()<fgThreeA):scoreA+=3
			else:
				if (random.random()<fgTwoA):scoreA+=2

			if random.random()<fracThrees:
				if (random.random()<fgThreeB):scoreB+=3
			else:
				if (random.random()<fgTwoB):scoreB+=2
		diff = scoreA-scoreB
		f2.write('%s\t%s\n' % (fracThrees,diff))
		if scoreA>scoreB:winner.append(0)
                elif scoreA<scoreB:winner.append(1)
                else:winner.append(0.5)
		
	upsetFreq = sum(winner)/float(len(winner))
	return upsetFreq

def simulateComeback(fracThrees,fgThreeB,attempts):
	#change freq of 3 attempts for only 1 team. Team A only takes 2s.
	#do more threes help a team comeback quickly from 20 point deficit...
	#f1 = open('comeback','w')
	#attempts = 20		#median 2014-15 season / 4
	fgThreeA = 0.3333
	#fgThreeB = 0.3333
	fgTwoA = 0.5
	fgTwoB = 0.5
	winner=[]
	for x in xrange(0,100000):
		scoreA=20
		scoreB=0
		for p in xrange(attempts):
			if random.random()<0.0:
				if (random.random()<fgThreeA):scoreA+=3
			else:
				if (random.random()<fgTwoA):scoreA+=2

			if random.random()<fracThrees:
				if (random.random()<fgThreeB):scoreB+=3
			else:
				if (random.random()<fgTwoB):scoreB+=2
		diff = scoreA-scoreB
		#f2.write('%s\t%s\n' % (fracThrees,diff))
		if scoreA>scoreB:winner.append(0)
                elif scoreA<scoreB:winner.append(1)
                else:winner.append(0.5)
		
	upsetFreq = sum(winner)/float(len(winner))
	return upsetFreq

if __name__ == '__main__':
	#fracThrees=0
	#while (fracThrees<=1):
	#	#gvb = simulateGvB(fracThrees)
	#	#gva = simulateGoodvsAve(fracThrees)
	#	#tvt = simulateTwovsThree(fracThrees)
	#	#ava = simulateAvevsAve(fracThrees)
	#	#print fracThrees, gvb, gva, tvt,ava
	#	cb = simulateComeback(fracThrees,0.333)
	#	cb2 = simulateComeback(fracThrees,0.5)
	#	print fracThrees, cb, cb2
	#	fracThrees+=0.025
	attempts = 10
	while (attempts<=100):
		cb = simulateComeback(1,0.333,attempts)
		print attempts, cb
		attempts+=1
	


