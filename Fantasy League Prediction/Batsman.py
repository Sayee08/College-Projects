import random
import csv
with open('batsman2.csv','wb') as csvfile:
    data=csv.writer(csvfile)
    count=0
    j=1
    while(count<840):
        matches=random.randint(1,20)
        runs=int(matches*(random.randint(20,47)+random.random()))
        average=float(runs)/float(matches)
        sr=random.randint(75,140)+random.random()
        nt=random.randint(1,matches)
        wickets=random.randint(0,((matches)*2))
        catches=random.randint(0,((matches)*2))
        ha=random.randint(0,1)
        opp=random.randint(0,7)
        fp=average+(nt*random.randint(0,4))+((catches*10)/matches)+((wickets*10)/matches)+int(sr/100)*10+(ha*matches*0.5)
        data.writerow([matches,runs,average,sr,nt,wickets,catches,ha,opp,fp])
        count=count+1
