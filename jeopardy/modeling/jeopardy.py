#!/usr/bin/python

# so this will be the master

from getData import *

def main():

	# download 
	getRawData()

	# model
	# I just made it in R. Code it to work in python.

	# tweet
	date, winningDays, winningDollars, gender, age, name, career, location = getCurrentStatus()
	features = {'date':date,'days':winningDays,'dollars':winningDollars,'gender':gender,'age':age,'name':name,'career':career,'location':location}
	predict(features)



if __name__ == "__main__":
	main()
