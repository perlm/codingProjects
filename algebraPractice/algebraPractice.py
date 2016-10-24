#!/usr/bin/python
import random


# I saw someone post a book of algebra practice questions. that's dumb. this is better

def play():
	while True:
		print "What game to play?\nAddition\nSubtraction\nMultiplication\nDivision\nWord Problem\n"
		game = raw_input().strip().lower()
		if game not in ("addition","subtraction","multiplication","division","word problem"):print "Invalid selection! %s" % (game)
		else:break

	while True:
		print "What Level?\n1 = Single Digit\n2 = Two Digit\n3 = Super Challenge\n"
		level = int(raw_input().strip())
		if level not in (1,2,3):print "Invalid selection! %s" % (level)
		elif level==3:
			level=10
			break
		else:break

	success=0
	for rep in xrange(5):
		a=random.randint(0,10**level)
		b=random.randint(0,10**level)

		if game=='addition':
			print "%i + %i = ?" % (a,b)	
			solution = a+b
		elif game=='subtraction':
			print "%i - %i = ?" % (a,b)	
			solution = a-b
		elif game=='multiplication':
			print "%i * %i = ?" % (a,b)	
			solution = a*b
		elif game=='division':
			if (a==0):a=1
			temp = a*b
			print "%i / %i = ?" % (temp,a)	
			#solution should be b.
			solution = temp/a
		elif game=='word problem':
			print "%i Pigs plus %i Pigs equals what?" % (a,b)	
			solution = str(a+b) + " Pigs".lower()

		if game!='word problem':response = int(raw_input().strip())
		else:response = str(raw_input().strip().lower())

		if response==solution:
			success+=1
			print "Correct! %i of %i correct!\n" % (success,rep+1)
		else:print "Wrong! Correct answer is %s. %i of %i correct!\n" % (solution,success,rep+1)


if __name__ == '__main__':
	play()
