library(MASS)
library(e1071)
library(stats)
fantasy_team<-matrix(NA,1,14)

##Batsman Prediction

batsman_data<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\batsman1.csv')
pairs(batsman_data[,1:(ncol(batsman_data)-1)])
model<-lm.ridge(FantasyPoint~Matches+Runs+Average+SR+X30I.s+Wickets+Catches+H.A+Opponent,batsman_data)
m<-matrix(0,nrow(batsman_data),ncol(batsman_data))
m[,1]<-1
m[,2:ncol(batsman_data)]<-as.matrix(batsman_data[,1:(ncol(batsman_data)-1)])
training_data_pred<- m %*% coef(model)
SSE<-0
SST<-0
for(i in 1:nrow(training_data_pred))
{
  SSE<-(training_data_pred[i,]-batsman_data[i,ncol(batsman_data)])**2+SSE
  SST<-(batsman_data[i,ncol(batsman_data)]-mean(batsman_data[,ncol(batsman_data)]))**2+SST
}
MSERR<-SSE/nrow(batsman_data)
RMSERR<-MSERR**(0.5)
r_squared_ridge<-(1-(SSE/SST))
test_data<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\IPL_2017_Batsman.csv')
m<-matrix(0,nrow(test_data),ncol(batsman_data))
m[,1]<-1
m[,2:ncol(m)]<-as.matrix(test_data[,1:ncol(test_data)])
test_data_pred<- m %*% coef(model)
modelsvm<-svm(FantasyPoint~Matches+Runs+Average+SR+X30I.s+Wickets+Catches+H.A+Opponent,batsman_data)
training_data_pred_svm<-as.matrix(predict(modelsvm,batsman_data[1:(ncol(batsman_data)-1)]))
SSE<-0
SST<-0
for(i in 1:nrow(training_data_pred_svm))
{
  SSE<-(training_data_pred_svm[i,]-batsman_data[i,ncol(batsman_data)])**2+SSE
  SST<-(batsman_data[i,ncol(batsman_data)]-mean(batsman_data[,ncol(batsman_data)]))**2+SST
}
MSESVM<-SSE/nrow(batsman_data)
RMSESVM<-MSESVM**(0.5)
r_squared_SVM<-(1-(SSE/SST))
test_data_pred_svm<-as.matrix(predict(modelsvm,test_data))
Batsman_t_Test<-t.test(test_data_pred_svm,NULL,"two.sided",mean(batsman_data[,ncol(batsman_data)]))
Player_name<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\Batsman_Name.csv')
Player_name<-as.matrix(Player_name)
if(r_squared_SVM>r_squared_ridge)
{
  for(i in 1:5){
    a<-which.max(test_data_pred_svm)
    fantasy_team[,i]<-Player_name[a]
    test_data_pred_svm<-test_data_pred_svm[-a]
    Player_name<-Player_name[-a]
  }
}
if(r_squared_SVM<r_squared_ridge)
{
  for(i in 1:5){
    a<-which.max(test_data_pred)
    fantasy_team[,i]<-Player_name[a]
    test_data_pred<-test_data_pred[-a]
    Player_name<-Player_name[-a]
  } 
}

##Bowler Prediction

bowler_data<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\bowler1.csv')
pairs(bowler_data[,1:(ncol(bowler_data)-1)])
model_bowler<-lm.ridge(Fantasy_Point~Matches+Wickets+Average+Eco+Nt+runs_scored+Catches+H.A+Opponent,bowler_data)
m<-matrix(0,nrow(bowler_data),ncol(bowler_data))
m[,1]<-1
m[,2:ncol(bowler_data)]<-as.matrix(bowler_data[,1:(ncol(bowler_data)-1)])
training_data_pred_bowler<- m %*% coef(model_bowler)
SSE<-0
SST<-0
for(i in 1:nrow(training_data_pred_bowler))
{
  SSE<-(training_data_pred_bowler[i,]-bowler_data[i,ncol(bowler_data)])**2+SSE
  SST<-(bowler_data[i,ncol(bowler_data)]-mean(bowler_data[,ncol(bowler_data)]))**2+SST
}
MSERR<-SSE/nrow(bowler_data)
RMSERR<-MSERR**(0.5)
r_squared_ridge<-(1-(SSE/SST))
test_data_bowler<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\IPL_2017_Bowler.csv')
m<-matrix(0,nrow(test_data_bowler),ncol(bowler_data))
m[,1]<-1
m[,2:ncol(m)]<-as.matrix(test_data_bowler[,1:ncol(test_data_bowler)])
test_data_pred_bowler<- m %*% coef(model)
modelsvm_bowler<-svm(Fantasy_Point~Matches+Wickets+Average+Eco+Nt+runs_scored+Catches+H.A+Opponent,bowler_data)
training_data_pred_svm_bowler<-as.matrix(predict(modelsvm_bowler,bowler_data[1:(ncol(bowler_data)-1)]))
SSE<-0
SST<-0
for(i in 1:nrow(training_data_pred_svm_bowler))
{
  SSE<-(training_data_pred_svm_bowler[i,]-bowler_data[i,ncol(bowler_data)])**2+SSE
  SST<-(bowler_data[i,ncol(bowler_data)]-mean(bowler_data[,ncol(bowler_data)]))**2+SST
}
MSESVM<-SSE/nrow(bowler_data)
RMSESVM<-MSESVM**(0.5)
r_squared_SVM<-(1-(SSE/SST))
test_data_pred_svm_bowler<-as.matrix(predict(modelsvm_bowler,test_data_bowler))
Bowler_t_Test<-t.test(test_data_pred_svm_bowler,NULL,"two.sided",mean(bowler_data[,ncol(bowler_data)]))
Player_name<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\Bowler_Name.csv')
Player_name<-as.matrix(Player_name)
if(r_squared_SVM>r_squared_ridge)
{
  for(i in 1:5){
    a<-which.max(test_data_pred_svm_bowler)
    fantasy_team[,(i+5)]<-Player_name[a]
    test_data_pred_svm_bowler<-test_data_pred_svm_bowler[-a]
    Player_name<-Player_name[-a]
  }
}
if(r_squared_SVM<r_squared_ridge)
{
  for(i in 1:5){
    a<-which.max(test_data_pred_bowler)
    fantasy_team[,(i+5)]<-Player_name[a]
    test_data_pred_bowler<-test_data_pred_bowler[-a]
    Player_name<-Player_name[-a]
  } 
}

## All-Rounder Prediction

allrounder_data<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\allrounder1.csv')
pairs(allrounder_data[,1:(ncol(allrounder_data)-1)])
model_allrounder<-lm.ridge(FantasyPoint~Matches+Runs+Average+SR+X30I.s+Wickets+Economy+Averageb+No.3WI.s+Catches+H.A+Opponent,allrounder_data)
m<-matrix(0,nrow(allrounder_data),ncol(allrounder_data))
m[,1]<-1
m[,2:ncol(allrounder_data)]<-as.matrix(allrounder_data[,1:(ncol(allrounder_data)-1)])
training_data_pred_allrounder<- m %*% coef(model_allrounder)
SSE<-0
SST<-0
for(i in 1:nrow(training_data_pred_allrounder))
{
  SSE<-(training_data_pred_allrounder[i,]-allrounder_data[i,ncol(allrounder_data)])**2+SSE
  SST<-(allrounder_data[i,ncol(allrounder_data)]-mean(allrounder_data[,ncol(allrounder_data)]))**2+SST
}
MSERR<-SSE/nrow(allrounder_data)
RMSERR<-MSERR**(0.5)
r_squared_ridge<-(1-(SSE/SST))
test_data_allrounder<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\IPL_2017_Allrounder.csv')
m<-matrix(0,nrow(test_data_allrounder),ncol(allrounder_data))
m[,1]<-1
m[,2:ncol(m)]<-as.matrix(test_data_allrounder[,1:ncol(test_data_allrounder)])
test_data_pred_allrounder<- m %*% coef(model_allrounder)
modelsvm_allrounder<-svm(FantasyPoint~Matches+Runs+Average+SR+X30I.s+Wickets+Economy+Averageb+No.3WI.s+Catches+H.A+Opponent,allrounder_data)
training_data_pred_svm_allrounder<-as.matrix(predict(modelsvm_allrounder,allrounder_data[1:(ncol(allrounder_data)-1)]))
SSE<-0
SST<-0
for(i in 1:nrow(training_data_pred_svm_allrounder))
{
  SSE<-(training_data_pred_svm_allrounder[i,]-allrounder_data[i,ncol(allrounder_data)])**2+SSE
  SST<-(allrounder_data[i,ncol(allrounder_data)]-mean(allrounder_data[,ncol(allrounder_data)]))**2+SST
}
MSESVM<-SSE/nrow(allrounder_data)
RMSESVM<-MSESVM**(0.5)
r_squared_SVM<-(1-(SSE/SST))
test_data_pred_svm_allrounder<-as.matrix(predict(modelsvm_allrounder,test_data_allrounder))
Allrounder_t_Test<-t.test(test_data_pred_svm_allrounder,NULL,"two.sided",mean(allrounder_data[,ncol(allrounder_data)]))
Player_name<-read.csv('D:\\studies\\V Sem\\Package\\Machine Learning\\Allrounder_Name.csv')
Player_name<-as.matrix(Player_name)
if(r_squared_SVM>r_squared_ridge)
{
  for(i in 1:4){
    a<-which.max(test_data_pred_svm_allrounder)
    fantasy_team[,(i+10)]<-Player_name[a]
    test_data_pred_svm_allrounder<-test_data_pred_svm_allrounder[-a]
    Player_name<-Player_name[-a]
  }
}
if(r_squared_SVM<r_squared_ridge)
{
  for(i in 1:4){
    a<-which.max(test_data_pred_allrounder)
    fantasy_team[,(i+10)]<-Player_name[a]
    test_data_pred_allrounder<-test_data_pred_allrounder[-a]
    Player_name<-Player_name[-a]
  } 
}