#!/usr/bin/python
from bs4 import BeautifulSoup
from datetime import datetime, date
import sys, time,re,requests

f1 = open('finals.data','w')

months=['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
BASE_URL = 'http://www.angelfire.com/mi4/malldirectories/wheel/{0}/{1}.html'
for y in xrange(2007, 2015):
	for m in months:
		r = requests.get(BASE_URL.format(y,m))
		table = BeautifulSoup(r.text).table
		try:
			for row in table.find_all('tr'):
				columns = row.find_all('td')
				try:
					match1 = re.search(r'[A-Z] [A-Z] [A-Z] [A-Z]',columns[3].text)
					match2 = re.search(r'[A-Z] [A-Z] [A-Z] [A-Z]',columns[2].text)
					if match1:
						answer = columns[2].text
						f1.write('{0}\n'.format(answer))
					elif match2:
						answer = columns[1].text
						f1.write('{0}\n'.format(answer))
					elif columns[2].text == 'PUZZLE':
						pass
					else:
						print 'line no work', columns[2].text, y, m
				except IndexError:
					pass
		except AttributeError:
			pass

