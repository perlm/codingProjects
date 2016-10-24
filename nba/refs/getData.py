# -*- coding: utf-8 -*-

import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, date
import requests, sys, time, re

# Parts of this adapted from https://github.com/danielfrg/nba/tree/master/src

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

def writeRefData():
        f1 = open('data/refFouls.data','w')
        f2 = open('data/refFoulsAve.data','w')

	refList={}
	gameList=[]
	#box score format changed for 2008-2009 season, +/- added.
	for year in xrange(2009,2015):gameList.extend(getGameList(year))
	#gameList = ['280220028']

	# box score
	# http://espn.go.com/nba/boxscore?gameId=400578306
	baseURL2 = 'http://espn.go.com/nba/boxscore?gameId={0}'
	# play by play
	# http://espn.go.com/nba/playbyplay?gameId=400578299&period=0
	#baseURL1 = 'http://espn.go.com/nba/playbyplay?gameId={0}&period=0'

	for i in gameList:
		fouls = []
		while True:
			try:
				r = requests.get(baseURL2.format(i))
				break
			except requests.ConnectionError:
				time.sleep(10)

		soup = BeautifulSoup(r.text)

		officialList = (re.search(r'Officials:</strong> ([A-Z\,\.\- ]*)<br/><strong>', unicode(soup), re.M|re.I))
		if not officialList:
			officialList = (re.search(r'Officials:</strong> ([A-Z\,\.\- ]*)<br/>', unicode(soup), re.M|re.I))

		if not officialList:
			print "No officials found!", i, soup
		else:
			offList= officialList.group(1)
			officials = map(str.strip, map(str, offList.split(',')))
			#if len(officials)==1:
			#	officials = map(str, offList.split(', '))

			for row in soup.find_all('tr'):
				columns = row.find_all('td')
				if (len(columns)>=12):
					temp = unicode(columns[12].getText())
					try:temp = int(temp)	#individual players have an int in +/- column
					except:fouls.append(int(columns[11].getText()))

			if len(fouls)==2:
				totalFouls = sum(fouls)
				for o in officials:
					try:
						if o not in refList:refList[o]=[totalFouls]
						else:refList[o].append(totalFouls)
					except TypeError:print o
			else:print "Didn't get 2 total pfs", len(fouls), i


	for ref in refList:
		name = ref.replace(' ', '-')
		f1.write('{0} {1}\n'.format(name, refList[ref]))

		count = len(refList[ref])
		ave = sum(refList[ref])/float(count)
		sd = 0
		for f in refList[ref]:sd += (ave - f)**2
		sd = (sd/float(count))**0.5
		f2.write('{0} {1} {2} {3}\n'.format(name, ave, sd, count))

	f1.close()
	f2.close()


if __name__ == '__main__':
	writeRefData()

