#!/usr/bin/python

##################################################
# solve a puzzle!
# http://fivethirtyeight.com/features/how-about-a-nice-game-of-chess/
##################################################

import random

def move():
	r = random.random()
	if r <= (1./3):
		return -1
	elif r <= (2./3):
		return 0
	else:
		return 1


def express(iterations=10000):
	#starting position is column 5.
	#how many distinct ways can end in column 5.
	# since there's no way to get back to 5 from off the board, don't need to worry about that
	success = []
	for i in xrange(iterations):
		path = ''
		p = 5
		for row in xrange(6):
			p = p + move()
			path += str(p)
		if p == 5:
			success.append(path)
	
	uniques = set(success)
	print "Attempts:",iterations, " Unique paths:",len(uniques)

def knight_move():
	# could generalize to fairy pieces
        r = random.random()
        if r <= (1./8):return (-2,-1)
        elif r <= (2./8):return (-2,1)
        elif r <= (3./8):return (2,-1)
        elif r <= (4./8):return (2,1)
        elif r <= (5./8):return (1,2)
        elif r <= (6./8):return (1,-2)
        elif r <= (7./8):return (-1,2)
	else:return(-1,-2)


def classic(iterations=10000):
	maxMoves = 0
	for it in xrange(iterations):
		#reset board
		board = [[0 for x in range(8)] for y in range(8)]
		#random start
		x = random.randint(0,7)
		y = random.randint(0,7)
		board[x][y]=1
		position = (x,y)
		while True:
			#make a move!
			(dx,dy) = knight_move()

			# check if off board
			if x + dx <0 or x + dx >7 or y + dy <0 or y + dy >7:break
			
			# check if intersects!
			# there's ambiguity -- does it move in x or y first? no way to distinguish.
			if abs(dx)==2:
				if board[x+int(dx/2)][y]==0:board[x+int(dx/2)][y]=1
				else:break
			if abs(dy)==2:
				if board[x][y+int(dy/2)]==0:board[x][y+int(dy/2)]=1
				else:break
			# ok, now I'm bored.




if __name__ == '__main__':
	express(10000000)
	# but this misses the possibility that the pawn can move twice in its first move!
