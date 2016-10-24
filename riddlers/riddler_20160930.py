#!/usr/bin/python

##################################################
# solve a puzzle!
# http://fivethirtyeight.com/features/cubs-world-series-puzzles-for-fun-and-profit/
# simulations are more fun!
##################################################

import random

def move_3way():
	r = random.random()
	if r <= (1./3):
		return -1
	elif r <= (2./3):
		return 0
	else:
		return 1

def win_or_lose(p=0.6):
	r = random.random()
	if r <= (p):
		return 'W'
	else:
		return 'L'

def play_series(games=7):
	end = round(float(games)/2)
	series = ''
	while True:
		series += str(win_or_lose())
		if series.count('W')==end or series.count('L')==end: break
	return series



def main(iterations=10000):
	# 3 series, best of 5, then 2 best of 7.
	# how many unique combos.
	success = []
	for i in xrange(iterations):
		path = ''
		path += str(play_series(5))
		path += str(play_series(7))
		path += str(play_series(7))
	
		if path.count('W')==11:
			success.append(path)
	
	uniques = set(success)
	#print uniques
	print "Attempts:",iterations, " Unique paths:",len(uniques)



if __name__ == '__main__':
	main(100000000)
