# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, string, time, re, os, sys

#####
# The objective of this script is to pull data from the Jeopardy archive so that it can analyzed and I can make a predictive model.
#####

def getNameDictionary():
	nameGenderDict={}
	nameAgeDict={}
	with open('/home/jason/nameImputation/namesAverage.data','r') as f1:
		for line in f1:
			cols = line.split()
			nameGenderDict[str(cols[0])]=str(cols[1])
			nameAgeDict[str(cols[0])]=float(cols[2])
	return nameGenderDict, nameAgeDict


def getSoup(url):
	while True:
		try:
			r = requests.get(url)
			break
		except requests.ConnectionError:time.sleep(1)
	return BeautifulSoup(r.text)



def getRawData():

	nameGenderDict, nameAgeDict = getNameDictionary() 

	baseURL1='http://www.j-archive.com/showgame.php?game_id={0}'

        if (os.path.exists('data/raw.data')):
                with open('data/raw.data','r') as f1:
                        for line in f1:
				start=int(line.split(',')[0])+1
                f1 = open('data/raw.data','a+')
        else:
                f1 = open('data/raw.data','w')
		start=0

	champDays=None
	champTotal=None
	champName=None

	skips = ["Tournament","Kids","College","School Week","Celebrity","Million Dollar Masters","Super Jeopardy","Three-way tie at zero","didn't have a winner"]

	for g in xrange(start,5300):
		url = (baseURL1.format(g))
	        r = getSoup(url)
		errorCheck = r.find('p', attrs={"class": "error"})
		tourCheck = r.find('div', attrs={"id":"game_comments"})
		
		if errorCheck:continue
		elif any(s in tourCheck.get_text() for s in skips):continue
		elif g==504 or g==1088 or g==1092 or g==1309:continue

		players=[]
		winningDays=None
		winningDollars=None
		career=None
		location=None
		returnChamp=None
		for p in r.findAll('p', attrs={"class": "contestants"}):
			intro= p.get_text().replace(',','')
			prevWin = (re.search(r'an? (.+) (originally )?from (.+) \(whose ([0-9]+)-day cash winnings total \$([0-9]+)\)$', unicode(intro), re.M|re.I))
			name = p.find('a')

			if prevWin:
				career=prevWin.group(1)
				location=prevWin.group(3)
				winningDays=int(prevWin.group(4))
				winningDollars=int(prevWin.group(5))
				returnChamp = name.get_text().encode('ascii', 'ignore')
			players.append(name.get_text().encode('ascii', 'ignore'))
		players = list(reversed(players))

		if (not winningDays) or (not winningDollars):
			print "No previous winner", g
			continue

		#get scores
		scores=[]
		for h3 in r.find_all('h3'):
			if h3.get_text() == 'Final scores:':
				following = h3.next.next.next
				for s in following.find_all('td', attrs={"class":['score_positive', 'score_negative']}):
					dollar= int(s.get_text().replace(',','').replace('$',''))
					if 'positive' in str(s):scores.append(dollar)
					elif 'negative' in str(s):scores.append(dollar*-1)

		if (len(scores)!=3):
			print "Error: no data", g
			continue

		#get winner - make sure it matches scores
		winner=None
		for w in r.find_all('td', attrs={"class": "score_remarks"}):
			if ('champion' in w.get_text()):
				winner=1
				break
			elif ('place' in w.get_text()):
				winner=2
				break
		else:print "No winner found!", g

		maxScore=-1
		win=-1
		for s in xrange(3):
			if (scores[s]>maxScore):
				maxScore=scores[s]
				win=s
		if (winner==1) and (win!=0):print "Error: not champion!", g
		if (winner==2) and (win==0):print "Error: not challenger!", g

		title = r.find('title').get_text()
		showNumber = (re.search(r'Show #([0-9]*), aired (.*)$', unicode(title), re.M|re.I))
		if showNumber:
			gameNumber = int(showNumber.group(1))
			date = showNumber.group(2).encode('ascii', 'ignore')
		else:
			print "Error: Not valid", g
			continue

		print "Adding game", g
		#get chammp info for summary
		if (date[0:4]=='2016'):
			champDays=None
			champTotal=None
			for w in r.find_all('td', attrs={"class": "score_remarks"}):
				if ('champion' in w.get_text()):
					if ('New' in w.get_text()):champDays=1
					else:
						getChampDays = (re.match('([0-9]+)-day champion', unicode(w.get_text()), re.M|re.I))
						champDays= int(getChampDays.group(1))
					getChampTotal = (re.search('champion: \$([0-9]+)$', unicode(w.get_text().replace(',','')), re.M|re.I))
					champTotal=int(getChampTotal.group(1))
					break
			champName = players[win]
			print "Champ Info:", champDays, champTotal, champName

		#first = players[win].split()[0]	# to get properties for winner
		first = returnChamp.split()[0]		# to get properties for returning champ
		gender = None
		age = None
		if first in nameGenderDict:gender = nameGenderDict[first]
		else:gender = 'U'
		if first in nameAgeDict:age = nameAgeDict[first]
		else:age = 36.8

		f1.write('{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n'.format(g, gameNumber, date, winningDays, winningDollars, winner, gender, age, returnChamp.replace(',',' '), career.replace(',',' '), location.replace(',',' ') ))

	return champDays, champTotal, champName


if __name__ == '__main__':
	getRawData()


