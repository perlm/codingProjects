# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests, string, time, re, os, collections
#import numpy as np
#from datetime import datetime, date

def getSoup(url):
	while True:
		try:
			r = requests.get(url)
			break
		except requests.ConnectionError:time.sleep(10)
	return BeautifulSoup(r.text)

def getNutrition(i):
	url = 'http://ndb.nal.usda.gov/ndb/foods/show/{0}?fgcd=&manu=&lfacet=&format=&count=&max=50&offset=0&sort=&qlookup='
	page = getSoup(url.format(i))
	n = page.find('div',attrs={"id":"view-name"}).get_text().encode('ascii', 'ignore').rstrip()
	n2 = re.search(r'[0-9], (.*)$', n, re.M|re.I)
	name = n2.group(1).replace(' ','_')
	print i, name

	nutrition = {}
	nutrients = []

	#nutrition = collections.OrderedDict()	#using ordereddict,so things are always in the same order. But each site is dif things!!!
	#nutrition['name']=name

	for tr in page.findAll('tr', attrs={"class": "odd"}):
		td=tr.findAll('td')
		nutrient = td[0].get_text().encode('ascii', 'ignore').rstrip()
		if name not in nutrition:
			nutrition[name]={}
			nutrition[name]['index']=i
		nutrition[name][nutrient]=float(td[2].get_text().encode('ascii', 'ignore'))
		nutrients.append(nutrient)

	return nutrition, nutrients


def buildFoodDictionary():
	#start=1
        #if (os.path.exists('data/foodFacts.data')):
        #        with open('data/foodFacts.data','r') as f1:
        #                for line in f1:
	#			try:start=int(line.split()[0])+1
	#			except ValueError:pass
        #        f1 = open('data/foodFacts.data','a+')
        #else:f1 = open('data/foodFacts.data','w')
        f1 = open('data/foodFacts.data','w')

	#need everything in memory, since each entry has different data...

	foods={}
	#nutrientSet = set()
	nutrientSet = collections.Counter()
	#for i in xrange(1,5):
	for i in xrange(1,8619):
		newFood = {}
		nutrientList=[]
		newFood, nutrientList = getNutrition(i)

		nutrientSet.update(nutrientList)
		foods.update(newFood)
		time.sleep(0.1)

	#now loop over foods at the end and print out
	f1.write('{0} '.format('Name'))
	for n in nutrientSet:
		#something wierd is going on, where someimtes the nutrient isn't stripped right.
		if nutrientSet[n]>6000:
			f1.write('{0} '.format(n))
			print n, nutrientSet[n]
	f1.write('\n')

	for f,v in foods.items():
		f1.write('{0} '.format(f))
		for n in nutrientSet:
			if nutrientSet[n]>6000:
				if n in foods[f]:f1.write('{0} '.format(foods[f][n]))
				else:f1.write('{0} '.format('N'))
		f1.write('\n')


	#for k,v in nutrition.items():f1.write('{0} '.format(v))


if __name__ == '__main__':
	buildFoodDictionary()
