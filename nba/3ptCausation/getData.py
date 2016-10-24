# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import requests, string, time, re, os
#import numpy as np
#from datetime import datetime, date

def getSoup(url):
	while True:
		try:
			r = requests.get(url)
			break
		except requests.ConnectionError:time.sleep(10)
	return BeautifulSoup(r.text)

def getTeamStats():
	f1 = open('data/teamStats.data','w')
	data={}
	f1.write('WPCT, FG3A, FGA, FG2PCT, FG3PCT, FTM, OREB, DREB, AST, TOV, STL, BLK, BLKA, PF, PTS, year, team\n')

	baseURL1 = 'http://stats.nba.com/stats/leaguedashteamstats?Conference=&DateFrom=&DateTo=&Division=&GameScope=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season=20{0}-{1}&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision='
	for year in xrange(0,15):
		yearEnd=year+1
		y1="%02d" % (year,)
		y2="%02d" % (yearEnd,)
		url = (baseURL1.format(y1,y2))
	        r = requests.get(url)

		rows = r.text.split('[')
		for row in rows:
			#print row
			#"TEAM_ID","TEAM_NAME","GP","W","L","W_PCT","MIN","FGM","FGA","FG_PCT","FG3M","FG3A","FG3_PCT","FTM","FTA","FT_PCT","OREB","DREB","REB","AST","TOV","STL","BLK","BLKA","PF","PFD","PTS","PLUS_MINUS","CFID","CFPARAMS"
			row=row.encode('ascii')
			c = row.split(',')
			stats=()
			try:
				twoPtMade = float(c[7])-float(c[10])
				twoPtAtt = float(c[8])-float(c[11])
				twoPtPer = twoPtMade/twoPtAtt
				stats= [c[5],c[11],c[8],twoPtPer,c[12],c[13],c[16],c[17],c[19],c[20],c[21],c[22],c[23],c[24],c[26]]
				map(float,stats)
				f1.write('{0}, {1}, {2}\n'.format(", ".join(map(str,stats)),y1, c[1]))
			except IndexError:pass
			except ValueError:pass

if __name__ == '__main__':
	getTeamStats()
