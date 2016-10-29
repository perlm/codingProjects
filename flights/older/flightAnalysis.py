import numpy as np
import pandas as pd
import scipy
#import matplotlib.pyplot as plt
import math

#data files come from http://openflights.org/data.html

def distance(lat1,lon1,lat2,lon2):
	y1 = math.radians(lon1)
	x1 = math.radians(lat1)
	y2 = math.radians(lon2)
	x2 = math.radians(lat2)
	dx = x2-x1
	dy = y2-y1
        a = (math.sin(dx/2.0))**2 + math.cos(x1) * math.cos(x2) * (math.sin(dy/2.0))**2
	c = 2 * math.atan2( math.sqrt(a), math.sqrt(1.0-a) )
	d = c * 3959.
	return d

vdistance = np.vectorize(distance)

#file1
cols=['Airline', 'Airline ID', 'Source airport', 'Source airport ID', 'Destination airport', 'Destination airport ID', 'Codeshare', 'Stops', 'Equipment']
routeData = pd.read_csv('routes.dat', sep=',', header=None, names=cols)

#file2
cols=['Airport ID', 'Name', 'City', 'Country', 'IATA/FAA', 'ICAO', 'Latitude', 'Longitude', 'Altitude', 'Timezone', 'DST', 'Tz database', 'time zone']
airportData = pd.read_csv('airports.dat', sep=',', header=None, names=cols)

#merge locations onto file2
merge1 = pd.merge(routeData, airportData, left_on='Source airport', right_on='IATA/FAA', right_index=False, sort=False, how='inner')
merge2 = pd.merge(merge1, airportData, left_on='Destination airport', right_on='IATA/FAA', right_index=False, sort=False, how='inner')
merge2['distance'] = vdistance(merge2['Latitude_y'],merge2['Longitude_y'],merge2['Latitude_x'],merge2['Longitude_x'])

merge3=merge2[['Source airport','Destination airport','Stops','City_x','Country_x','City_y','Country_y','distance']]

#just continental:
europe = ['Albania', 'Andorra', 'Armenia', 'Austria', 'Azerbaijan','Belarus','Belgium','Bosnia and Herzegovina','Bulgaria','Croatia','Cyprus','Czech Republic','Denmark','Estonia','Finland','France','Germany','Greece','Hungary','Italy','Kosovo','Latvia','Liechtenstein','Lithuania','Luxembourg','Macedonia','Moldova','Monaco','Montenegro','Netherlands','Norway','Poland','Portugal','Romania','San Marino','Serbia','Slovakia','Slovenia','Spain','Sweden','Switzerland','Turkey','Ukraine']

USdata= merge3.groupby(['Country_x', 'Country_y']).get_group(('United States', 'United States'))
Chinadata= merge3.groupby(['Country_x', 'Country_y']).get_group(('China', 'China'))
Brazildata= merge3.groupby(['Country_x', 'Country_y']).get_group(('Brazil', 'Brazil'))

columns = ['Source airport','Destination airport','Stops','City_x','Country_x','City_y','Country_y','distance']
Europedata= pd.DataFrame(columns=columns)
for country1 in europe:
	for country2 in europe:
		try:
			tempData = merge3.groupby(['Country_x', 'Country_y']).get_group((country1, country2))
			Europedata=pd.concat([Europedata,tempData])
		except KeyError:
			pass

#print merge3['distance'].describe()
#print USdata['distance'].describe()
#print Chinadata['distance'].describe()
#print Brazildata['distance'].describe()
#print Europedata['distance'].describe()

count,division = np.histogram(merge3['distance'], bins=np.arange(0,9000,50))
countU,divisionU = np.histogram(USdata['distance'], bins=np.arange(0,9000,50))
countC,divisionC = np.histogram(Chinadata['distance'], bins=np.arange(0,9000,50))
countB,divisionB = np.histogram(Brazildata['distance'], bins=np.arange(0,9000,50))
countE,divisionE = np.histogram(Europedata['distance'], bins=np.arange(0,9000,50))
for x in xrange(len(count)):
	print division[x], count[x], countU[x], countC[x], countB[x], countE[x]

