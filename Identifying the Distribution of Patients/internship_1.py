from threading import Thread
from Queue import Queue
import csv
import sys
import gmplot
mapping=[]
tempmap=[]
cnt=0
def fetchFromGoogle(inq):

    from tornado import ioloop, httpclient
    import time
    from urlparse import urlparse
    def handle_request(response):
        result=response.body
        pincode=str(urlparse(response.effective_url).query[8:14])
        global cnt
        cnt-=1
        try:
            result=result[result.find(" \"location\" ")+14:]
            result=result[:result.find("},")+1]
            lat=float(result[result.find(":")+1:result.find(",")].strip())
            longi=float(result[result.find("\"lng\" :")+7:result.find("}")].strip())
            mapping.append([pincode,lat,longi])
        except:
            print pincode,"Not Found"
        if cnt==0:
            try:
                with open("pincode.csv", "ab") as f:
                    writer = csv.writer(f)
                    writer.writerows(mapping)
            except:
                print "Error in Printing to file"
                
            ioloop.IOLoop.instance().stop()
            print "Finished"

    http_client = httpclient.AsyncHTTPClient()
    while True:
      if not inq.empty():
        tic=time.time()
        url='https://maps.googleapis.com/maps/api/geocode/json?address='+inq.get()+'&components=IN&key=AIzaSyAl5XqsdVzwCZW8oJuPiWIIxHHYMq6OCvs'
        inq.task_done()
        global cnt
        cnt+=1
        http_client.fetch(url.strip(), handle_request)
      if time.time()-tic>5:
         break;
    ioloop.IOLoop.instance().start()


def fetchFromFile(values,outq):

    try:
         with open('pincode.csv','rb') as f:
            reader=csv.reader(f)
            pincode=list(reader)
         togetcoord=list(set(values)-set(zip(*pincode)[0]))
         temp=list(set(values).intersection(zip(*pincode)[0]))
         global tempmap
         tempmap=map(lambda x:pincode[zip(*pincode)[0].index(x)],temp)
         if len(tempmap)!=0:
                map(lambda x:outq.put(x),togetcoord)
         else:
                map(lambda x:outq.put(x),set(values))
    except Exception,e:
         print str(e)
         map(lambda x:outq.put(x),set(values))

def joinDatas(givendata,mapping,count):

    import pandas as pd
    givendata=pd.DataFrame(givendata,columns=["Pincode","Date","Dept"])
    mapping=pd.DataFrame(mapping,columns=["Pincode","Lat","Long"])
    count=pd.DataFrame(count,columns=["Pincode","Frequency"])
    givendata=givendata.merge(mapping,on='Pincode').merge(count,on='Pincode')
    tomap=givendata.groupby(["Date","Lat","Long","Pincode"]).size().reset_index(name="cnt")
    return tomap

def select(tomap):
    end=tomap.Date.max()
    start=tomap.Date.min()
    print('Start Date : '+start+'\nEnd Date : '+end)
    #Enter dates like this :'01-07-2017'
    #Exceptional Handling to be done for dates
    start_date=input('Enter Start Date In DD-MM-YYYY format:')
    end_date=input('Enter End Date In DD-MM-YYYY format:')
    l=tomap['Date']>=start_date
    u=tomap['Date']<=end_date
    tomap=tomap[l&u]
    return tomap

def printToMap(tomap):
    count_pincode=tomap.groupby('Pincode')['cnt'].sum()
    Lat=tomap.groupby('Pincode')['Lat'].unique()
    Lon=tomap.groupby('Pincode')['Long'].unique()
    mean=count_pincode.mean()
    std=count_pincode.std()
    CLat=tomap.Lat[tomap['Pincode']=='641004'].unique()
    CLon=tomap.Long[tomap['Pincode']=='641004'].unique()#Lat and Long Of Peelamedu
    Lat1=[];Lat2=[];Lat3=[];Lat4=[];Lon1=[];Lon2=[];Lon3=[];Lon4=[]
    gmap = gmplot.GoogleMapPlotter(CLat[0],CLon[0],15)
    for i in xrange(0,len(count_pincode)):
            if(count_pincode[i]<mean-std):
                Lat1.append(float(Lat[i][0]))
                Lon1.append(float(Lon[i][0]))
            elif(count_pincode[i]<mean):
                Lat2.append(float(Lat[i][0]))
                Lon2.append(float(Lon[i][0]))   
            elif(count_pincode[i]>mean):
                Lat3.append(float(Lat[i][0]))
                Lon3.append(float(Lon[i][0]))
            else:        
                Lat4.append(float(Lat[i][0]))
                Lon4.append(float(Lon[i][0]))
    gmap.scatter(Lat1,Lon1,'#98AFC7',size=500,marker=False)
    gmap.scatter(Lat2,Lon2,'#7BCCB5',size=500,marker=False) 
    gmap.scatter(Lat3,Lon3,'#FFA500',size=500,marker=False)
    gmap.scatter(Lat4,Lon4,'#FF0000',size=500,marker=False)
    gmap.draw('map.html')
    return


if __name__=='__main__':

    givendata=[]
    with open("sample.csv", 'rb') as f:
         reader = csv.DictReader(f)
         givendata = list(reader)
    values=map(lambda x:x["Pincode"],givendata)
    count=map(lambda x:[x,values.count(x)],set(values))
    q=Queue()
    thread1 = Thread(target = fetchFromFile,args=(values,q,))
    thread1.start()
    thread2 = Thread(target = fetchFromGoogle,args=(q,))
    thread2.start()
    thread2.join()
    thread1.join()
    q.join()
    mapping+=tempmap
    tomap=joinDatas(givendata,mapping,count)
    tomap=select(tomap)
    printToMap(tomap)
