import random
import csv
with open('allrounder2.csv','wb') as csvfile:
    data=csv.writer(csvfile)
    count=0
    j=1
    while(count<320):
        matches=random.randint(1,20)
        runs=int(matches*(random.randint(10,35)+random.random()))
        average=float(runs)/float(matches)
        sr=random.randint(75,140)+random.random()
        nt=random.randint(1,matches)
        ntw=random.randint(1,matches)
        runs_given=int(matches*(random.randint(10,55)))
        wickets=random.randint(2,((matches)*3))
        averageb=float(runs_given)/float(wickets)
        eco=random.randint(7,9)+random.random()
        catches=random.randint(0,((matches)*2))
        ha=random.randint(0,1)
        opp=random.randint(0,7)
        fp=int((1/averageb)*100)+average+(nt*random.randint(0,4))+((catches*10)/matches)+((wickets*10)/matches)+int(sr/100)*10+(ha*matches*0.5)+(ntw*random.randint(0,4))+int((1/eco)*100)
        data.writerow([matches,runs,average,sr,nt,wickets,eco,averageb,ntw,catches,ha,opp,fp])
        count=count+1
