#!/usr/bin/python

from twitter import *
import ConfigParser

def tweetProb(features):
	tweet = '{n} is a {day}-day champ with ${dol} winnings: #Jeopardy model predicts {p}% prob to win! (as of {date}) https://hastydata.wordpress.com/2016/11/26/modeling-jeopardy-revisited/'.format(n=str(features['name']), day=str(features['days']),dol=str(features['dollars']),p=int(100*round(float(features['prob']),2)),date=str(features['date']) )

	config = ConfigParser.ConfigParser()
	config.read('/home/jason/.pythontwitter')

	t = Twitter(auth=OAuth(token=config.get('section','token'), token_secret=config.get('section','token_secret'), consumer_key=config.get('section','consumer_key'), consumer_secret=config.get('section','consumer_secret')))
	t.statuses.update(status=tweet)

	print "Tweet Sent:\n%s" % (str(tweet))


if __name__ == '__main__':
	features = {}
	tweetProb(features)



