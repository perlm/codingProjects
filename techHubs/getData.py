# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, sys, time, re, datetime, operator, random, urllib, os 

def getCities(cityFile='UScities.data'):
       	f1 = open(cityFile,'r')
	cityLocation={}
	for line in f1:
		cols = re.split(r'\t+', line)
		#city names occur twice. use location for first, which is the biggest.
		if cols[0] not in cityLocation:
			cityLocation[cols[0]] = (cols[1],cols[2])
	return cityLocation
	f1.close()

def getPopularity():
       	f1 = open('techhub.data','w')

	cityLocation={}
	cityLocation = getCities()

	for city in cityLocation:
		line = city + ' "tech hub"'
		linePlus = line.replace(' ', '+')

		#bing: but bing sucks: try binging Yea
		#searchTerm = 'http://www.bing.com/search?q=%2B"%28' + linePlus + '%29"'

		#google: knows I'm a robot.
		searchTerm = 'http://www.google.com/search?q=' + linePlus

		#yahoo: knows I'm a robot
		#searchTerm = 'http://www.de.search.yahoo.com/search?p=+"' + linePlus + '"'

		#mywebsearch: knows I'm a robot
		#searchTerm = 'http://www.search.mywebsearch.com/mywebsearch/searchfor="' + linePlus

		#aol search: knows I'm a robot?
		#searchTerm = 'http://search.aol.com/aol/search?s_it=topsearchbox.search&v_t=na&q=' + linePlus

		print searchTerm

		while True:
			try:
				r = requests.get(searchTerm)
				break
			except requests.ConnectionError:
				print "search sleeping", datetime.datetime.time(datetime.datetime.now())
				sleepTime = random.uniform(41, 101)
				time.sleep(sleepTime)

		soup = BeautifulSoup(r.text)
		#aol:
		#results = soup.find('div', attrs={"id": "result-count"})
		#results = str(results)
		#m = re.search(r'([0-9,]+) results', results)

		soup = str(soup)
		#print soup
		m = None
		m = re.search(r'About ([0-9,]+) results', soup)
		cityName = city.replace(' ','_')
		if (m):
			number = int(m.group(1).replace(',',''))
                        f1.write('{0} {1} {2} {3} {4}\n'.format(cityName, number, cityLocation[city][0],cityLocation[city][1], searchTerm))
		else:f1.write('{0} 0 {2} {3} {4}\n'.format(cityName, cityLocation[city][0],cityLocation[city][1], searchTerm))

		sleepTime = random.uniform(20, 30)
		time.sleep(sleepTime)
	
	f1.close()

if __name__ == '__main__':
	getPopularity()

