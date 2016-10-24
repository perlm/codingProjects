import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, date
import requests, sys, time, re

# partially adapted from https://github.com/danielfrg/nba/tree/master/src

# Collects and organizes play by play data from ESPN.

def teamList():
        url = 'http://espn.go.com/nba/teams'
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'html.parser')
        tables = soup.findAll('ul')

        prefix_1 = []
        prefix_2 = []
        for table in tables:
            lis = table.find_all('li')
            for li in lis:
                if li.h5:
                        info = li.h5.a
                        url = info['href']
                        prefix_1.append(url.split('/')[-2])
                        prefix_2.append(url.split('/')[-1])
        return prefix_1,prefix_2


def getGameList(year):
	#get list of all teams
	prefix_1,prefix_2 = teamList()

	#get list of games from team schedule:
	gameID=[]

	if (year == 2014):
		baseURL1 = 'http://espn.go.com/nba/team/schedule/_/name/{0}/seasontype/2/{1}'	#regular season
		#baseURL2 = 'http://espn.go.com/nba/team/schedule/_/name/{0}/{1}'		#post-season
		for t in xrange(len(prefix_1)):
	                while True:
                        	try:
					r = requests.get(baseURL1.format(prefix_1[t], prefix_2[t]))
					break
				except requests.ConnectionError:time.sleep(10)
			table = BeautifulSoup(r.text).table
			if table:
				for row in table.find_all('tr')[1:]:
					columns = row.find_all('td')
	        			try:
						gameID.append(columns[2].a['href'].split('?id=')[1])
					except Exception as e:pass
			else:pass
	else:
		baseURL1 = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/seasontype/2/{2}'
		for t in xrange(len(prefix_1)):
	                while True:
                        	try:
					r = requests.get(baseURL1.format(prefix_1[t],year,prefix_2[t]))
                                	break
                        	except requests.ConnectionError:time.sleep(10)

			table = BeautifulSoup(r.text).table
			if table:
				for row in table.find_all('tr')[1:]: # Remove header
					columns = row.find_all('td')
	        			try:
						gameID.append(columns[2].a['href'].split('?id=')[1])
					except Exception as e:pass
			else:pass

	gameID = list(set(gameID))	#remove overlap
	expected = int(82*30*0.5)
	if (expected != len(gameID)):print "Error: Wrong Number of Matches! %s" % (len(gameID))
	return gameID

def writeGameDataMinutes(year):
        f1 = open('gameData_%s.data' % (year),'w')

	gameList = getGameList(year)
	#gameList = ['400578456', '400578306']

	# box score
	# http://espn.go.com/nba/boxscore?gameId=400578306
	#BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
	# play by play
	# http://espn.go.com/nba/playbyplay?gameId=400578299&period=0
	baseURL1 = 'http://espn.go.com/nba/playbyplay?gameId={0}&period=0'

	for i in gameList:
		gameData=[]
		visitor = 0
		home = 0
		winner = 0
		Quarter = 1
		previousTime=1000
		previousScore=0
		overTime=0	#ignore overtime for now

		while True:
			try:
				r = requests.get(baseURL1.format(i))
				break
			except requests.ConnectionError:
				time.sleep(10)

		soup = BeautifulSoup(r.text)
		for row in soup.find_all('tr'):
			columns = row.find_all('td')
			times=[];score=[]
			try:
				times = re.search(r'([0-9]{1,2}:[0-9][0-9])', columns[0].getText(), re.M|re.I)
				score = re.search(r'([0-9]{1,3}-[0-9]{1,3})', columns[2].getText(), re.M|re.I)
			except IndexError:pass
			if (times and score and winner!=0):
				timeLeftInQuarter= int(times.group(1)[:-3])
				if timeLeftInQuarter > previousTime:Quarter+=1
				if Quarter==5:break	#overtime?

				actualTime = (12*(Quarter-1)) + (12-timeLeftInQuarter) 

				for t in xrange(0,actualTime):
					n = len(gameData)
					if n<=t:
						gameData.append([previousScore, winner])

				scores =score.group(1).split('-')
				scoreDifferential = int(scores[1])-int(scores[0])	#home-away

				previousTime = timeLeftInQuarter
				previousScore = scoreDifferential
			else:
				final=[]
				try:
					if 'OT' in columns[5].getText():overTime=1
					final = re.search(r'([0-9]{2,3})', columns[5].getText(), re.M|re.I)
				except IndexError:pass

				if (final and visitor==0):
					visitor=int(final.group(1))
				elif (final and home==0):
					home=int(final.group(1))
					if (home>visitor):winner=1
					elif (home<visitor):winner=-1
					elif (overTime==1):winner=0
					else:print "Error: no winner? %s %s %s " % (i, home, visitor, )

					if winner==1 or winner==-1:gameData = [[0,winner]]

				elif (home>0 and final):print "Error: third score found %s %s %s " % (i, home, visitor)

		if (len(gameData)==48):
			for ttt,rrr in enumerate(gameData):f1.write('{0} {1} {2}\n'.format(ttt,rrr[0],rrr[1]))
	f1.close()


if __name__ == '__main__':
	for year in xrange(2008,2015):
	        writeGameDataMinutes(year)

