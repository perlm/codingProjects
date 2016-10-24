# -*- coding: utf-8 -*-

import sys
sys.path.append("/home/jason/Desktop/Dropbox/personal/jeopardy/predicting/")

from getData import getRawData
from buildModel import processData
from buildModel import buildLogisticRegressionPolynomial
import subprocess

def tweetProb():
	champDays, champTotal,champName = getRawData()
	#champDays,champTotal,champName= 1, 20000, 'Pete'
	if (champDays) and (champTotal):
		prob = buildLogisticRegressionPolynomial(3,True,champDays,champTotal)
		p = prob*100

		tweet = '%s is a %s-day champ with \$%s winnings: \#Jeopardy model predicts %.1f%% prob to win! https://t.co/Y6yYQNn8gl' % (str(champName), str(champDays), str(champTotal),float(p))

		print "Tweet Sent: %s" % (str(tweet))
		print len(tweet)
		command = "/usr/local/bin/twitter set %s" % (str(tweet))
		subprocess.call(command, shell=True)
	else:print "Error: no new data"

if __name__ == '__main__':
	tweetProb()



