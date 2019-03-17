from threading import Thread
from Queue import Queue
import csv
import sys
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
    return givendata

def printToMap(givendata):

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
    givendata=joinDatas(givendata,mapping,count)
    printToMap(givendata)
