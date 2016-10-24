import requests
import pandas as pd
from bs4 import BeautifulSoup

def teamList():
	url = 'http://espn.go.com/nba/teams'
	r = requests.get(url)

	soup = BeautifulSoup(r.text, 'html.parser')
	#tables = soup.findAll('ul', class_='medium-logos')
	tables = soup.findAll('ul')
        #tables = BeautifulSoup(soup.text).find(class_='medium-logos')
        #tables = BeautifulSoup(soup.text,'lxml')

	prefix_1 = []
	prefix_2 = []
	for table in tables:
	    lis = table.find_all('li')
	    for li in lis:
		if li.h5:
		        info = li.h5.a
		        #teams.append(info.text)
	        	url = info['href']
	        	prefix_1.append(url.split('/')[-2])
	        	prefix_2.append(url.split('/')[-1])


	#dic = {'prefix_2': prefix_2, 'prefix_1': prefix_1}
	#teams = pd.DataFrame(dic, index=teams)
	#teams.index.name = 'name'
	#print prefix_1,prefix_2

	return prefix_1,prefix_2

if __name__ == '__main__':
        teamList()

