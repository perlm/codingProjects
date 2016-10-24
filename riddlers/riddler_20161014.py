#!/usr/bin/python

##################################################
# solve a puzzle!
# http://fivethirtyeight.com/features/can-you-survive-this-deadly-board-game/
##################################################

import random

def express(l=100):
	# index 1-100. skip index=0
	coins = [0] + [1]*l


	#for each round
	for r in xrange(1,l+1):
		#check each coin
		for c in xrange(1,l+1):
			if c % r == 0:
				coins[c] = coins[c] * -1
				print r, c
	down = []
	for c in xrange(1,l+1):
		if coins[c] == 1:coins[c]='H'
		else:
			down.append(c)
			coins[c]='T'
	print coins[1:]
	print down

def classic_density(iterations=1000):
	# just for fun ---- what is the density of hits across the board
	# it peaks at 6! That is somewhat interesting. Steady state well before 1000
	board = [0] * 1001
	for i in xrange(iterations):
		pos = 0
		while pos<=1000:
			board[pos]+= 1
			pos += random.randint(1,6)

	for i,p in enumerate(board):
		d = float(p)/iterations
		print i,d

def gen_combinations(combinations, max_position):
	positions=[]
	for x in xrange(combinations):
		a = random.randint(1,max_position)
		b = random.randint(1,max_position)
		c = random.randint(1,max_position)
		if a==b or a==c or b==c:continue
		l = sorted([a,b,c])
		positions.append(tuple(l))
	return list(set(positions))

def classic(iterations=100,*args):

	boardLength 	= 20

	# first generate combination of spots
	if len(args)==1:
		combinations = gen_combinations(args[0],boardLength)
	else:
		combinations = args


	# for each combination, walk the board
	combos 		= {}
	for ccc in combinations:
		death = 0
		for i in xrange(iterations):
			pos 	= 0
			while pos<boardLength:
				if pos in ccc:break
				pos += random.randint(1,6)
			else:death+=1
		rate = 1 - float(death)/iterations
		combos[ccc] = rate
	
	for w in sorted(combos, key=combos.get, reverse=True):
		print w, combos[w]





if __name__ == '__main__':
	# this is not efficient, but should be fine.
	#express(100)
	#classic_density(1000)


	# retrospect- I got 4-6-8 for best non-consecutive, but the author reports 6-8-10!
	# rewrote code to accept either number of random combinations to generate, 
	# or a pre-defined list of combinations, so I can test two with more iterations quickly.
	iterations=1000000
	#combinations=500
	#classic(iterations,combinations)
	classic(iterations,(4,6,8),(6,8,10))

	# After a million iterations--- turns out the author was right!
	#(6, 8, 10) 0.714396
	#(4, 6, 8) 0.711975



