# -*- coding: utf-8 -*-
"""
Created on Thu Nov 15 00:10:35 2018

@author: soham
"""
#!pip install textblob
#!pip install vadersentiment





import pandas
import seaborn as sns
import numpy as np
sns.set_style('darkgrid')
from numpy import loadtxt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyze = SentimentIntensityAnalyzer()


csvfile='russiadata.newversion.csv'
adataframe=pandas.read_csv(csvfile)

adataframe1=adataframe[['Ad Text ','Ad Impressions ','Ad Clicks ','Ad Spend ','campaign length','begindateobject','enddateobject']]
adataframe=adataframe.dropna()
adataframe.reset_index()
adataframe=adataframe.reindex(index=range(0,2603))



fb_text=adataframe['Ad Text ']

fb_text.reset_index()
fb_text=fb_text.reindex(index=range(0,2603))        



s1 = []
s2 = []
s3 = []
s4 = []
s5 = []
s6 = []


for i in range(len(fb_text)):
    s1.append(TextBlob(str(fb_text.loc[[i]])).polarity)
    s6.append(TextBlob(str(fb_text.loc[[i]])).subjectivity)

for i in range(len(fb_text)):
    s2.append(analyze.polarity_scores(str(fb_text.loc[[i]]))['neg'])
    s3.append(analyze.polarity_scores(str(fb_text.loc[[i]]))['neu'])
    s4.append(analyze.polarity_scores(str(fb_text.loc[[i]]))['pos'])
    s5.append(analyze.polarity_scores(str(fb_text.loc[[i]]))['compound'])
     
    

adataframe1=adataframe[['Ad Text ','Ad Impressions ','Ad Clicks ','Ad Spend ','campaign length','begindateobject','enddateobject']]

column_values = pandas.Series(s1)
adataframe1.insert(loc=0, column='Polarity', value=column_values)

column_values = pandas.Series(s2)
adataframe1.insert(loc=0, column='Negative_Score', value=column_values)

column_values = pandas.Series(s3)
adataframe1.insert(loc=0, column='Neutral_Score', value=column_values)

column_values = pandas.Series(s4)
adataframe1.insert(loc=0, column='Positive_Score', value=column_values)

column_values = pandas.Series(s5)
adataframe1.insert(loc=0, column='Compound_Sensitivity_Score', value=column_values)

column_values = pandas.Series(s6)
adataframe1.insert(loc=0, column='Subjectivity', value=column_values)


adataframe2=adataframe1[['Ad Text ','Ad Impressions ','Ad Clicks ','Ad Spend ','campaign length','begindateobject','enddateobject','Polarity','Subjectivity','Negative_Score','Neutral_Score','Positive_Score','Compound_Sensitivity_Score']]   

adataframe2=adataframe2.dropna()

adataframe3=adataframe2[['Ad Text ','Ad Clicks ','Ad Spend ','campaign length','begindateobject','enddateobject','Polarity','Subjectivity','Negative_Score','Neutral_Score','Positive_Score','Compound_Sensitivity_Score']]   

adataframe3=adataframe3.dropna()




adataframe3.to_csv("Predective_Cha2.csv", index=False, header=True)

adataframe3[['Negative_Score','Neutral_Score','Positive_Score','Compound_Sensitivity_Score']].plot.bar(rot=0)

#import statsmodels.api as sm

#X = adataframe1['Ad Impressions ']
#y = adataframe1['campaign length']

#model = sm.OLS(y.astype(float), X.fit())



