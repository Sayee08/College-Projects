import csv
import gmplot
import json
import requests
def getcoordinates(i):
    try:
            url='https://maps.googleapis.com/maps/api/geocode/json?address='+i
            r = requests.get(url)
            lat,longi=r.json()['results'][0]['geometry']['location'].values()

            return lat,longi,i
    except:
	    #print str(i)
	    return 0,0,i
    

with open("sample.csv", 'rb') as f:
         reader = csv.DictReader(f)
         givendata = list(reader)
         
values=map(lambda x:x["Pincode"],givendata)
data=map(lambda p:list(getcoordinates(p)),set(values))
lat=[]
lon=[]
for row in xrange(0,len(givendata)):
        for i in data:
            if givendata[row]["Pincode"]==i[2]:
                    lat.append(i[0])
                    lon.append(i[1])
                    givendata[row]["Lat"],givendata[row]["long"]=i[0],i[1]
                    
gmap = gmplot.GoogleMapPlotter(lat[0],lon[0],18)
gmap.scatter(lat[1],lon[1], '#000000', size=10, marker=False)
gmap.draw('map.html')

