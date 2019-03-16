# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 20:05:27 2018

@author: soham
"""
import pandas as pd
df = pd.read_csv('Travel Pony Facebook.csv')
df.count

# Remove rows that have amount spent = 0 as 
#these campaigns didnot start

df1 = df[df['Amount Spent (USD)'] != 0]
df1.count

# 1. Next, graph a histogram of Amount Spent using Seaborn
import seaborn as sns
sns.set_style('darkgrid')
sns.distplot(df1['Amount Spent (USD)'])

# 2. Build a multiple regression where the outcome variable is Amount Spent and the
#  predictor variables are:
#Campaign Name
#Reach
#Frequency
#Impressions
#Clicks
#Unique Clicks
#Amount Spent (USD)
#Page Likes
#Page Engagement
#Post Engagement
#Post Likes
#Post Comments
#Post Shares
#Photo Views
#Website Clicks
# Make sure that you convert "Campaign Name" to some type of categorical value that the
# regression understands as such.
df1['Campaign Name'] = df1['Campaign Name'].astype('category')
df1['Campaign Code'] = df1['Campaign Name'].cat.codes
X = df1[['Campaign Code','Reach','Frequency','Impressions','Clicks','Unique Clicks','Page Likes', 'Page Engagement', 'Post Engagement', 'Post Likes', 'Post Comments', 'Post Shares', 'Photo Views', 'Website Clicks']]

import statsmodels.api as sm
X=sm.add_constant(X)
y = df1['Amount Spent (USD)']
X.shape
linreg = sm.OLS(y,X).fit()
linreg.summary()

 

# 3. Look at the coefficients for each one of your predictor variables. The
# higher the value, the stronger predictive value the variable has with
# amount spent. That is, when we spend more, we tend to get more of this
# variable than anything else.
# What are the three predictors with the highest predictive value
# (rank them, please).
#Ans:
#As per the Coeff  Page Likes,Page Engagement,Post Engagement have high effect 
#on predictor variable
#But if we check the P values  Clicks,Post Likes and Photo Views 
#are stronger predictive value for amount spent


