import random
import csv
with open('bowler2.csv','wb') as csvfile:
    data=csv.writer(csvfile)
    count=0
    j=1
    while(count<840):
        matches=random.randint(1,20)
        runs_given=int(matches*(random.randint(10,55)))
        wickets=random.randint(2,((matches)*4))
        average=float(runs_given)/float(wickets)
        eco=random.randint(5,9)+random.random()
        nt=random.randint(1,matches)
        catches=random.randint(0,((matches)*2))
        runs_scored=int(matches*(random.randint(0,20)+random.random()))
        ha=random.randint(0,1)
        opp=random.randint(0,7)
        fp=int((1/average)*100)+wickets+(nt*random.randint(0,4))+((catches*10)/matches)+((runs_scored*10)/matches)+int((1/eco)*100)+(ha*matches*0.5)
        data.writerow([matches,wickets,average,eco,nt,runs_scored,catches,ha,opp,fp])
        count=count+1
