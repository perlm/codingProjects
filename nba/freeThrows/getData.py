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

def writeFreeThrows():
        f1 = open('data/freeThrows.data','w')
        f2 = open('data/techSwitches.data','w')

	ftMakes1={}
	ftAttempts1={}
	ftMakes2={}
	ftAttempts2={}
	ftMakes3={}
	ftAttempts3={}

	nameList=[]
	gameList=[]
	for year in xrange(2008,2015):gameList.extend(getGameList(year))
	#gameList = ['400793122']

	# box score
	# http://espn.go.com/nba/boxscore?gameId=400578306
	#BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
	# play by play
	# http://espn.go.com/nba/playbyplay?gameId=400578299&period=0
	baseURL1 = 'http://espn.go.com/nba/playbyplay?gameId={0}&period=0'

	for i in gameList:
		while True:
			try:
				r = requests.get(baseURL1.format(i))
				break
			except requests.ConnectionError:
				time.sleep(10)
		techTeam=None
		techShooter=None
	

		soup = BeautifulSoup(r.text)
		for row in soup.find_all('tr'):
			columns = row.find_all('td')
			try:
				if 'free throw' in columns[1].getText() or 'free throw' in columns[3].getText():
					player=None
					make=None
					number=None

					if 'free throw' in columns[1].getText():
						ftPlay= (re.search(r'(.*) (makes|misses)', columns[1].getText(), re.M|re.I))
						player=ftPlay.group(1)
						if ftPlay.group(2) == 'makes':make=1
						else:make=0
						if ' of ' in columns[1].getText():
							getNum= (re.search(r'([0-9]) of [0-9]', columns[1].getText(), re.M|re.I))
							try:number=int(getNum.group(1))
							except AttributeError:
								number=1
								print columns
						else:number=1

						if 'technical' in columns[1].getText():
							techShooter=player
							techTeam=1
							techMake=make
						elif (techShooter) and (techTeam==1):
							nameS = techShooter.replace(' ', '-')
							nameP = player.replace(' ', '-')
							try:f2.write('{0} {1} {2} {3} {4} {5}\n'.format(nameS, techMake, nameP, make, number, i))
							except UnicodeEncodeError:pass
					elif 'free throw' in columns[3].getText():
						ftPlay= (re.search(r'(.*) (makes|misses)', columns[3].getText(), re.M|re.I))
						player=ftPlay.group(1)
						if ftPlay.group(2) == 'makes':make=1
						else:make=0
						if ' of ' in columns[3].getText():
							getNum= (re.search(r'([0-9]) of [0-9]', columns[3].getText(), re.M|re.I))
							try:number=int(getNum.group(1))
							except AttributeError:
								number=1
								print columns
						else:number=1

						if 'technical' in columns[3].getText():
							techShooter=player
							techTeam=2
							techMake=make
						elif (techShooter) and (techTeam==2):
							nameS = techShooter.replace(' ', '-')
							nameP = player.replace(' ', '-')
							try:f2.write('{0} {1} {2} {3} {4} {5}\n'.format(nameS, techMake, nameP, make, number, i))
							except UnicodeEncodeError:pass
					if (number==1):
						if player in ftAttempts1:ftAttempts1[player]+=1
						else: ftAttempts1[player]=1
						if (make==1):
							if player in ftMakes1:ftMakes1[player]+=1
							else: ftMakes1[player]=1
					elif (number==2):
						if player in ftAttempts2:ftAttempts2[player]+=1
						else: ftAttempts2[player]=1
						if (make==1):
							if player in ftMakes2:ftMakes2[player]+=1
							else: ftMakes2[player]=1
					elif (number==3):
						if player in ftAttempts3:ftAttempts3[player]+=1
						else: ftAttempts3[player]=1
						if (make==1):
							if player in ftMakes3:ftMakes3[player]+=1
							else: ftMakes3[player]=1
					else:print "Error: ", number

					if player not in nameList:nameList.append(player)
				elif 'enters the game' not in columns[1].getText() and 'enters the game' not in columns[3].getText():
					#subs happen between FT
					techTeam=None
					techShooter=None
			except IndexError:pass

	for p in nameList:
		try:m1=ftMakes1[p]
		except KeyError:m1=0
		try:m2=ftMakes2[p]
		except KeyError:m2=0
		try:m3=ftMakes3[p]
		except KeyError:m3=0
		try:a1=ftAttempts1[p]
		except KeyError:a1=0
		try:a2=ftAttempts2[p]
		except KeyError:a2=0
		try:a3=ftAttempts3[p]
		except KeyError:a3=0
		name = p.replace(' ', '-')
		try:f1.write('{0} {1} {2} {3} {4} {5} {6}\n'.format(name, m1, a1, m2, a2, m3, a3))
		except UnicodeEncodeError:pass

	
	f1.close()


if __name__ == '__main__':
	        writeFreeThrows()

