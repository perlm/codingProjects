# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, string, time, re, os

# Scraping NBA.com using the strategy suggested by: http://www.gregreda.com/2015/02/15/web-scraping-finding-the-api/

def getSoup(url):
	while True:
		try:
			r = requests.get(url)
			break
		except requests.ConnectionError:time.sleep(10)
	return BeautifulSoup(r.text)



def getPlayerStats():
        f1 = open('3andD.data','w')
	data={}
	players=[]

	baseURL1 = 'http://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=20{0}-{1}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='
	baseURL2 = 'http://stats.nba.com/stats/leaguedashplayerstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=Totals&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=20{0}-{1}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
	for year in xrange(14,15):
		yearEnd=year+1

		url = (baseURL1.format(year,yearEnd))
	        r = requests.get(url)
		rows = r.text.split('[')
		for row in rows:
			cols = row.split(',')
			if len(cols)>2:
				nameCol = cols[1]
				name = None
				name = (re.search(r'"([A-Z].*)"', unicode(nameCol), re.M|re.I))
				if (name):players.append(name.group(1))
				else:print "Error: Name not found: ", nameCol
                                data[(name.group(1),'threePer')] = cols[13]
                                data[(name.group(1),'threeMade')] = cols[15]
			
		url = (baseURL2.format(year,yearEnd))
	        r = requests.get(url)
		rows = r.text.split('[')
		for row in rows:
			cols = row.split(',')
			if len(cols)>2:
				nameCol = cols[1]
				name = None
				name = (re.search(r'"([A-Z].*)"', unicode(nameCol), re.M|re.I))
				if (name) and (name.group(1) not in players):print "Error: Name not in list!", nameCol
				elif (not name):print "Error: Name not found2: ", nameCol
                                else:data[(name.group(1),'defRTG')] = cols[11]

	for p in players:
		#f1.write('{0} {1} {2}\n'.format(data[p,'threePer'],data[p,'threeMade'], p))
		try:
			pr = p.replace(' ','_')
			f1.write('{0} {1} {2} {3}\n'.format(data[p,'threePer'],data[p,'threeMade'], data[p,'defRTG'], pr))
		except:print p
	#return data, players


if __name__ == '__main__':
	getPlayerStats()
