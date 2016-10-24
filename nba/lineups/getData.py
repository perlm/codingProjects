# -*- coding: utf-8 -*-

# A simple python script to scrape data from different nba statistics websites and provide nicely formatted data.
# The goal here was to consider how different combinations of 5-man lineup player heights relate to performance.

from bs4 import BeautifulSoup
import requests, string, time, re, os
#import numpy as np
#from datetime import datetime, date

# Scraping NBA.com using the strategy suggested by: http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/
# some code borrowed from https://github.com/andrewgiessel/basketballcrawler

def getSoup(url):
	while True:
		try:
			r = requests.get(url)
			break
		except requests.ConnectionError:time.sleep(10)
	return BeautifulSoup(r.text)

def lineupHeight():
	f1 = open('data/lineupHeightStats.data','w')
	data,lineups = getLineupsStats()

	playerHeight={}
        if (os.path.exists('data/playerHeight.data')):
		print "Reading heights from file"
		with open('data/playerHeight.data','r') as ph:
			for line in ph:
				cols = line.split(',')
				#names from nba and nba-ref sometimes have periods?
				name = cols[0].replace(".","")
				playerHeight[name]=cols[1]
	else:
		print "Getting Heights from internet"
		playerHeight=buildPlayerDictionary()

	gsw = 6*12+7
	#for index, lu in enumerate(lineups):
	#for index, lu in enumerate(players.items()):
	for lu in lineups:
		lineupHeight=[]
		for player in lu.split(" "):
			if "," in player:
				pcols = player.split(',')
				playerName = str(pcols[1]).replace('"','').replace(".","") + " " + str(pcols[0])

				#for names that changed...
				if 'Barea' in playerName:playerName='Jose Barea'
				elif 'Amundson' in playerName:playerName='Louis Amundson'
				elif 'Jeff Taylor'==playerName:playerName='Jeffery Taylor'
				playerName = playerName.replace('Jr.','Jr')

				if playerName in playerHeight:
					ph = int(playerHeight[playerName])
					lineupHeight.append(ph)
				else: print "Error: player not in height database! ", playerName

		r1=0
		r2=0
		lineupMean = sum(lineupHeight)/float(len(lineupHeight))
		for h in lineupHeight:
			r1 += (h-gsw)**2
			r2 += (h-lineupMean)**2
		r1 = (r1/5.0)**0.5
		r2 = (r2/5.0)**0.5
			
		f1.write('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n'.format(r1,r2,data[(lu,'off')], data[(lu,'def')],data[(lu,'oppEFG')], data[(lu,'oppTO')], data[(lu,'oppORB')],data[(lu,'oppSEC')], data[(lu,'oppFBP')], data[(lu,'oppPIP')], lu))

def getLineupsStats():
	data={}
	lineups=[]
	playersYear=None
	offense=None
	defense=None
	oppEFG=None
	oppTO=None
	oppORB=None
	oppSEC=None
	oppFBP=None
	oppPIP=None

	baseURL1 = 'http://stats.nba.com/stats/leaguedashlineups?DateFrom=&DateTo=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Per48&Period=0&PlusMinus=N&Rank=N&Season=20{0}-{1}&SeasonSegment=&SeasonType=Regular+Season&VsConference=&VsDivision='
	baseURL2 = 'http://stats.nba.com/stats/leaguedashlineups?DateFrom=&DateTo=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Four+Factors&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Per48&Period=0&PlusMinus=N&Rank=N&Season=20{0}-{1}&SeasonSegment=&SeasonType=Regular+Season&VsConference=&VsDivision='
	baseURL3 = 'http://stats.nba.com/stats/leaguedashlineups?DateFrom=&DateTo=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Misc&Month=0&OpponentTeamID=0&Outcome=&PaceAdjust=N&PerMode=Per48&Period=0&PlusMinus=N&Rank=N&Season=20{0}-{1}&SeasonSegment=&SeasonType=Regular+Season&VsConference=&VsDivision='
	for year in xrange(10,15):
		yearEnd=year+1

		url = (baseURL1.format(year,yearEnd))
	        r = requests.get(url)
		rows = r.text.split('[')
		for row in rows:
			cols = row.split('","')
			if (cols[0]=='"Lineups'):
				players1= re.sub(r'".*','',cols[2])
				players = players1.split(' - ')
				#lineups.append(players[:5])
				players = map(str, players)
				playersYear = ' '.join(players[:5]) + " " + str(year)
				lineups.append(playersYear)

				cols2 = row.split(',')
				data[(playersYear,'off')] = cols2[15]
				data[(playersYear,'def')] = cols2[16]

		url = (baseURL2.format(year,yearEnd))
	        r = requests.get(url)
		rows = r.text.split('[')
		for row in rows:
			cols = row.split('","')
			if (cols[0]=='"Lineups'):
				players1= re.sub(r'".*','',cols[2])
				players = players1.split(' - ')
				players = map(str, players)
				playersYear = ' '.join(players[:5]) + " " + str(year)

				cols2 = row.split(',')
				data[(playersYear,'oppEFG')] = float(cols2[19])
				data[(playersYear,'oppTO')] = float(cols2[21])
				data[(playersYear,'oppORB')] = float(re.sub(r'[^\d.]+','',cols2[22]))

		url = (baseURL3.format(year,yearEnd))
	        r = requests.get(url)
		rows = r.text.split('[')
		for row in rows:
			cols = row.split('","')
			if (cols[0]=='"Lineups'):
				players1= re.sub(r'".*','',cols[2])
				players = players1.split(' - ')
				players = map(str, players)
				playersYear = ' '.join(players[:5]) + " " + str(year)

				cols2 = row.split(',')
				data[(playersYear,'oppSEC')] = float(cols2[20])
				data[(playersYear,'oppFBP')] = float(cols2[21])
				data[(playersYear,'oppPIP')] = float(re.sub(r'[^\d.]+','',cols2[22]))
	return data, lineups

def getCurrentPlayerNamesAndURLS(supressOutput=True):
	names = []
	for letter in string.ascii_lowercase:
		letter_page = getSoup('http://www.basketball-reference.com/players/%s/' % (letter))

		#current_names=[]
		# we know that all the currently active players have <strong> tags, so we'll limit our names to those
		current_names = letter_page.findAll('strong')
		#print current_names
		for n in current_names:
			name_data = n.children.next()
			names.append((name_data.contents[0], 'http://www.basketball-reference.com' + name_data.attrs['href']))

		# if I want inactive players also:
		table = letter_page.table
		if (table):
			for entry in table.findAll('tr'):
				columns= entry.findAll('td')
				if len(columns)>3:
					n = columns[0]
					name_data = n.children.next()
					try:names.append((name_data.contents[0], 'http://www.basketball-reference.com' + name_data.attrs['href']))
					except:
						pass
						#n2 = n.find('a')
						#names.append((name_data.contents[0], 'http://www.basketball-reference.com' + n2.attrs['href']))
					#print name_data.contents[0], name_data.attrs['href']

		time.sleep(1) # sleeping to be kind for requests

	return dict(names)

def buildPlayerDictionary():
	f1 = open('data/playerHeight.data','w')
	playerNamesAndURLS = getCurrentPlayerNamesAndURLS()
	players={}
	for name, url in playerNamesAndURLS.items():
		players[name] = {'overview_url':url}
		players[name]['overview_url_content'] = None
		players[name]['height'] = None
	
	for i, (name, player_dict) in enumerate(players.items()):
		if players[name]['overview_url_content'] is None:
			overview_soup = getSoup(players[name]['overview_url'])
			players[name]['overview_url_content'] = overview_soup.text

			text = players[name]['overview_url_content'].encode('ascii', 'ignore')

			heightMatch = None
			#Height: 7-0Weight
			heightMatch = (re.search(ur'Height: ([0-9])-([0-9]{1,2})W', text, re.M|re.I|re.U))
			if (heightMatch):
				#print heightMatch.group(0)
				height = int(heightMatch.group(1))*12 + int(heightMatch.group(2))
				f1.write('{0}, {1}\n'.format(name,height))
				players[name]['height']=height
			else:
				print "Error: No match for ", name

		time.sleep(1)
	return players

if __name__ == '__main__':
	#lineupHeight()
	lineupHeight()
