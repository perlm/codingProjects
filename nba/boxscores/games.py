import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import sys, time, re

f1 = open('Gasols.data','w')

#get list of all teams
from teams import teamList
prefix_1,prefix_2 = teamList()

match_id = []
BASE_URL1 = 'http://espn.go.com/nba/team/schedule/_/name/{0}/seasontype/2/{1}'	#regular season
BASE_URL2 = 'http://espn.go.com/nba/team/schedule/_/name/{0}/{1}'		#post-season

if isinstance(prefix_1, basestring):
	#if prefix_1 is a string (i.e. defines 1 team)
	r = requests.get(BASE_URL.format(prefix_1, prefix_2))
	table = BeautifulSoup(r.text).table
	for row in table.find_all('tr')[1:]: # Remove header
		columns = row.find_all('td')
	        try:
			match_id.append(columns[2].a['href'].split('?id=')[1])
		except Exception as e:
			pass # Not all columns row are a match, is OK
#elif True:pass
else:
	#if prefix_1 is a list (i.e. defines many teams)
	for t in xrange(len(prefix_1)):
		r = requests.get(BASE_URL1.format(prefix_1[t], prefix_2[t]))
		table = BeautifulSoup(r.text).table
		if table:
			for row in table.find_all('tr')[1:]: # Remove header
				columns = row.find_all('td')
	        		try:
					match_id.append(columns[2].a['href'].split('?id=')[1])
				except Exception as e:
					pass
		else:
			pass
		r = requests.get(BASE_URL2.format(prefix_1[t], prefix_2[t]))
		table = BeautifulSoup(r.text).table
		if table:
			for row in table.find_all('tr')[1:]: # Remove header
				columns = row.find_all('td')
	        		try:
					match_id.append(columns[2].a['href'].split('?id=')[1])
				except Exception as e:
					pass
		else:
			pass
match_id = list(set(match_id))	#remove overlap
print "Total Number of matches: ", len(match_id)

# http://espn.go.com/nba/boxscore?gameId=400578306
BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
##get column headers for player statistics
#r = requests.get(BASE_URL.format(match_id[0]))
#table = BeautifulSoup(r.text).find('table', class_='mod-data')
#heads = table.find_all('thead')
#headers = heads[0].find_all('tr')[1].find_all('th')[1:]
#headers = [th.text for th in headers]
##columns = ['id', 'team', 'player'] + headers
#columns = ['player'] + headers

def get_gasols(players):
    gasols=0
    for i, player in enumerate(players):
        cols = player.find_all('td')
	name = cols[0].text
	test = cols[1].text
	if ('Gasol' in name) and ('DNP' not in test):
		gasols=1
    return gasols

def get_playerStats(players, columns):
    allStatistics=[]
    allStatistics.append(columns)
    for i, player in enumerate(players):
        cols = player.find_all('td')
	stats=[]
	for j in xrange(20):
		try:
			stats.append(cols[j].text)
		except:
			pass
	allStatistics.append(stats)
    return allStatistics

def get_teamStats(team_stats):
    statistics=[]
    for i, stats in enumerate(team_stats):
	cols = stats.find_all('td')
	for j in xrange(15):
		try:
			statistics.append(cols[j].text)
		except:
			pass
    return statistics
		
#match_id = ['400578306','400578301','400579075','400579169']	#to test on single game
gasol={}
games={}

for i in match_id:
	run = None
	while run is None:
                        try:
				request = requests.get(BASE_URL.format(i))
				table = BeautifulSoup(request.text,'lxml')
				parsedP = table.find_all('p')
				d = re.search(r'ET, ([A-Z].* 201[45])', parsedP[7].text, re.M|re.I)
				date = d.group(1)
				heads = table.find_all('thead')
				team_1 = heads[0].th.text
				team_2 = heads[3].th.text
				bodies = table.find_all('tbody')
				gasols=0
				if (team_1 == 'Chicago Bulls') or (team_1 == 'Memphis Grizzlies'):
					team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
					gasols += get_gasols(team_1_players)
				if (team_2 == 'Chicago Bulls') or (team_2 == 'Memphis Grizzlies'):
					team_2_players = bodies[3].find_all('tr') + bodies[4].find_all('tr')
					gasols += get_gasols(team_2_players)
				if date in gasol:gasol[date] += gasols
				else:gasol[date]=gasols
				if date in games:games[date] += 1
				else:games[date] = 1
				run=1
			except requests.ConnectionError:
				print "fail,", i
                                time.sleep(60)
                        except:
				print "Unexpected error for match",i,  sys.exc_info()[0]
				run=1

for d in games:
	#print d, games[d], gasol[d]
	f1.write('"{0}"\t{1}\t{2}\n'.format(str(d),str(games[d]),str(gasol[d])))

	#print rebounds and opposing fg%
	#team_stats = bodies[2].find_all('tr')
	#statistics1=get_teamStats(team_stats)
	#team_stats = bodies[5].find_all('tr')
	#statistics2=get_teamStats(team_stats)
	#f1.write('{0}\t{1}\t{2}\t{3}\n'.format(statistics1[6], statistics2[15], statistics2[6], statistics1[15]))
	#print fg% and 3-fg% for Starting PG and SG:
	#for t in xrange(2):
	#	if t==0:team = bodies[0].find_all('tr')# + bodies[3].find_all('tr')	#this would get starters for both teams
	#	elif t==1:team = bodies[3].find_all('tr')
	#	statistics = get_playerStats(team, columns)
	#	pg=[]
	#	sg=[]
	#	for row in statistics:
	#		if ', PG' in row[0] and len(row)>5:
	#			shots = map(float, row[2].split('-'))
	#			shotsThree = map(float, row[3].split('-'))
	#			if (shots[1]>0):pg.extend([ shots[0]/shots[1]])
	#			if (shotsThree[1]>0):pg.extend([shotsThree[0]/shotsThree[1]])
	#		elif ', SG' in row[0] and len(row)>5:
	#			shots = map(float, row[2].split('-'))
	#			shotsThree = map(float, row[3].split('-'))
	#			if (shots[1]>0):sg.extend([ shots[0]/shots[1]])
	#			if (shotsThree[1]>0):sg.extend([shotsThree[0]/shotsThree[1]])
	#	if len(pg)==2 and len(sg)==2:
        #	        f1.write('{0}\t{1}\t{2}\t{3}\n'.format(str(pg[0]),str(pg[1]),str(sg[0]),str(sg[1])))
	#	#else:
	#	#	print i

	#print fg% and 3-fg% for Thomson and Curry:
	#if (team_1 == 'Golden State Warriors'):
	#	team_1_players = bodies[0].find_all('tr') + bodies[1].find_all('tr')
	#	statistics = get_playerStats(team_1_players, columns)
	#elif (team_2 == 'Golden State Warriors'):
	#	team_2_players = bodies[3].find_all('tr') + bodies[4].find_all('tr')
	#	statistics = get_playerStats(team_2_players, columns)
	#curry=[]
	#thompson=[]
	#for row in statistics:
	#	if row[0] == 'Stephen Curry, PG' and len(row)>5:
	#		shots = map(float, row[2].split('-'))
	#		shotsThree = map(float, row[3].split('-'))
	#		if (shots[1]>0):curry.extend([ shots[0]/shots[1], shotsThree[0]/shotsThree[1]])
	#	elif row[0] == 'Klay Thompson, SG' and len(row)>5:
	#		shots = map(float, row[2].split('-'))
	#		shotsThree = map(float, row[3].split('-'))
	#		if (shots[1]>0):thompson.extend([shots[0]/shots[1], shotsThree[0]/shotsThree[1]])
	#if len(curry)>0 and len(thompson)>0:
	#	print curry[0], curry[1], thompson[0], thompson[1]

	#print fg% and 3-fg% for GSW teams:
	#if (team_1 == 'Golden State Warriors'):
	#	team_stats = bodies[2].find_all('tr')
	#	statistics=get_teamStats(team_stats)
	#	print statistics[15],statistics[16]
	#elif (team_2 == 'Golden State Warriors'):
	#	team_stats = bodies[5].find_all('tr')
	#	statistics=get_teamStats(team_stats)
	#	print statistics[15],statistics[16]


