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

def getPace():

	gameList=[]
	#box score format changed for 2008-2009 season, +/- added.
	for year in xrange(2009,2010):
		gameList.extend(getGameList(year))
		#gameList = ['400578306']

		teamPace={}
		gamePace=[]

		# have to estimate number of posessions from boxscore:
		# http://www.nba.com/celtics/stats/inside-the-numbers/points-per-possession-pop-up.html
		# Number of possessions =  ((FGA - O-Rebs) + TO + (.436 x FTA))
		# Average two teams to get game pace?
	
        	f1 = open('data/games_%s.data' % (year),'w')
        	f2 = open('data/seasonAve_%s.data' % (year),'w')

		# box score
		# http://espn.go.com/nba/boxscore?gameId=400578306
		baseURL2 = 'http://espn.go.com/nba/boxscore?gameId={0}'
		# play by play
		# http://espn.go.com/nba/playbyplay?gameId=400578299&period=0
		#baseURL1 = 'http://espn.go.com/nba/playbyplay?gameId={0}&period=0'

		for i in gameList:
			while True:
				try:
					r = requests.get(baseURL2.format(i))
					break
				except requests.ConnectionError:
					time.sleep(10)

			soup = BeautifulSoup(r.text)
			FGA1, FGA2, FTA1, FTA2, ORB1, ORB2, TO1, TO2=0,0,0,0,0,0,0,0
			TEAM1, TEAM2 ="",""
	
			for row in soup.find_all('tr'):
				columns = row.find_all('td')
				try:
					if (columns[2].getText() == "Final") and (not TEAM1):TEAM1 = str(columns[0].getText())
					elif (columns[2].getText() == "Final") and (not TEAM2):TEAM2 = str(columns[0].getText())
				except IndexError:pass
				if (len(columns)>=12):
					temp = unicode(columns[12].getText())
					try:temp = int(temp)	#individual players have an int in +/- column
					except:
						if (not FGA1):
							TO1 = int(columns[10].getText())
							ORB1 = int(columns[4].getText())
							FG = columns[1].getText().split('-')
							FGA1 = int(FG[1])
							FT = columns[3].getText().split('-')
							FTA1 = int(FT[1])
						else:
							TO2 = int(columns[10].getText())
							ORB2 = int(columns[4].getText())
							FG = columns[1].getText().split('-')
							FGA2 = int(FG[1])
							FT = columns[3].getText().split('-')
							FTA2 = int(FT[1])

			#((FGA - O-Rebs) + TO + (.436 x FTA))
			if (FGA1) and (FGA2) and (TEAM1) and (TEAM2):
				P1 = (FGA1 - ORB1) + TO1 + (0.436 * FTA1)
				P2 = (FGA2 - ORB2) + TO2 + (0.436 * FTA2)
				pace = (P1 + P2)/2.0
				#print FGA1, ORB1, TO1, FTA1
				#print FGA2, ORB2, TO2, FTA2
				#print TEAM1, TEAM2, pace
				gamePace.append([TEAM1, TEAM2, pace])
				if TEAM1 not in teamPace:teamPace[TEAM1]=[pace]
				else:teamPace[TEAM1].append(pace)
				if TEAM2 not in teamPace:teamPace[TEAM2]=[pace]
				else:teamPace[TEAM2].append(pace)

		teamPaceAve={}
		for team in teamPace:
			name = team.replace(' ', '-')
			count = len(teamPace[team])
			ave = sum(teamPace[team])/float(count)
			teamPaceAve[team] = ave
			f2.write('{0} {1}\n'.format(name, ave))

		for g in xrange(len(gamePace)):
			p1 = teamPaceAve[gamePace[g][0]]
			p2 = teamPaceAve[gamePace[g][1]]
			f1.write('{0} {1} {2} {3} {4}\n'.format(p1, p2, gamePace[g][2], gamePace[g][0], gamePace[g][1]))
	
		f1.close()
		f2.close()


if __name__ == '__main__':
	getPace()

