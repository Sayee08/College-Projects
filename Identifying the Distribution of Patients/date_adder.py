import random
import csv
with open('sample1.csv','wb') as csvfile:
    data=csv.writer(csvfile)
    count=0
    j=1
    while(count<16230):
        r=random.randint(400,500)
        if(r+count>16230):
                r=16230-count
        for i in xrange(0,r):
                j=random.randint(1,31)
                data.writerow([str(j)+'-06-2017'])
        count=count+r
        #j=int(j)+1
		#if(j>31):
                    
		
