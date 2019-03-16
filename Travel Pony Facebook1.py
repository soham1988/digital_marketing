# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 17:11:02 2018

@author: soham
"""
#When considering 'cost per impression', what day of the week works best? (What day is it cheapest to generate impressions) 
#What day works worst? (What day is most expensive)

import pandas as pd

import arrow


df = pd.read_csv('Travel Pony Facebook.csv')


df['cost per impression']=df['Amount Spent (USD)']/df['Impressions']

    
weekday_map={2:'Mon',3:'Tue',4:'Wed',5:'Thu',6:'Fri',0:'Sat',1:'Sun'}

weekdays=[]
for i,r in df.iterrows():
	 ad=arrow.get(r['Start Date'],'M/D/YY')
	 weekdays.append(weekday_map[ad.weekday()])


df['weekdays']=pd.Series(weekdays)

print("Best day of week:",df['weekdays'][df['cost per impression'].idxmin()],";cost per impression",df['cost per impression'][df['cost per impression'].idxmin()])
print("Worst day of week:",df['weekdays'][df['cost per impression'].idxmax()],";cost per impression",df['cost per impression'][df['cost per impression'].idxmax()])

#Using Pivot table on the dataframe

weekday_pivoteddata = df.pivot_table(index='weekdays', aggfunc='mean')

#Converting pivot table to dataframe

dw=pd.DataFrame(weekday_pivoteddata,columns=['cost per impression','weekday'])
print("Best day of week:",dw['cost per impression'].idxmin(),";cost per impression",dw['cost per impression'][dw['cost per impression'].idxmin()])
print("Worst day of week:",dw['cost per impression'].idxmax(),";cost per impression",dw['cost per impression'][dw['cost per impression'].idxmax()])





#Next, compute the correlation (Links to an external site.)
#Links to an external site. between Amount Spent and the following variables:
#- Reach
#- Frequency 
#- Unique Clicks
#- Page Likes
#Which correlation is the strongest? 
#What does that mean practically? (respond in a tweet or less)


m=df.corr()
a=m['Reach']['Amount Spent (USD)']
b=m['Frequency']['Amount Spent (USD)']
c=m['Unique Clicks']['Amount Spent (USD)']
d=m['Page Likes']['Amount Spent (USD)']

data={'variable':['Reach','Frequency','Unique Clicks','Page Likes'],'correlation':[a,b,c,d]}
j=pd.DataFrame(data,columns=['variable','correlation'])
    

print("Amount Spent (USD) max correlation is with ",j['variable'][j['correlation'].idxmax()],"=",j['correlation'][j['correlation'].idxmax()],"\n","Change Amount Spent (USD) high positive effect on",j['variable'][j['correlation'].idxmax()]," with great positive relationship")



#Finally, perform a simple multiple regression analysis (Links to an external site.)Links to an external site. 
#where Unique Clicks is the dependent variable 
#and Reach and Frequency are the independent (predictor) variables.
#What variable most strongly predicts unique clicks? 
#What does that mean practically? (respond in a tweet or less)
 
from sklearn import linear_model

x1=df[['Reach','Frequency']]
y1=df['Unique Clicks']
regr = linear_model.LinearRegression()
regr.fit(x1, y1)
regr.score(x1, y1)
print('Intercept: \n', regr.intercept_)
print('Coefficients: \n', regr.coef_)

import statsmodels.api as sm

x1=df[['Reach','Frequency']]
y1=df['Unique Clicks']
model = sm.OLS(y1, x1).fit()
model.summary()


##############
#1)Best day of week: Mon ;cost per impression 1.3117197697515264
#Worst day of week: Sun ;cost per impression 2.05663914118258

#2)Amount Spent (USD) max correlation is with  Unique Clicks = 0.8829931774784341 
#To increase Unique Clicks there should be more amount sent.

#3)As 'Unique Clicks' has positive coefficient so it will increase w.r.t 'Reach' .
#As 'Unique Clicks' has negative coefficient so it will decrease w.r.t 'Frequency' .
###############


    
 


   