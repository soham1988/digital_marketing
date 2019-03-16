##!/usr/bin/env python2
## -*- coding: utf-8 -*-
#"""
#Created on Fri Jul 14 14:15:43 2017
#
#@author: cvargo
#"""
import csv
#from time import sleep
import re
import numpy as np
from scipy import stats
import seaborn as sns
import pickle
sns.set(color_codes=True)

#this function extracts dollar amounts from the social media posts
def get_all_money_from_string(text):
    """Return a list of the dollar amounts from the
    text string or the empty list if none is found."""
    
    dollar_re = r'\$[0-9,]+'
    return re.findall(dollar_re, text)


#loads in the social media data       
masterdict = pickle.load(open('giveaway.exampledata.p','rb'))


#creating a dict and and list of all giveaway amounts
moneydict = {}
allmonies = []

##simple counter for the number of promotions
count = 0
##simple counter for the number of promotions that have dollar amounts
dollarcount = 0

##iterating through each facebook post in the data
for apost in masterdict:
    ##pulling out the post and setting it to a dictionary so we can take a look
    thepost = masterdict[apost]
    
    ##looking at the promotion probability dict entry to see if the post
    ##is indeed a promotion
    ##if the score is greater than .5864, it's a likely a promotion
    if float(thepost['apromotion']) > 0.5864:
        #ticking up our promotion count        
        count += 1
        ##doing a quick check to see if $ amount is mentioned
        if '$' in thepost['text']:
            #tick up the dollar count by one
            dollarcount += 1
            #use get_all_money function to extract dollar amounts
            dollaramounts = get_all_money_from_string(thepost['text'])
            #dollaramounts is a list, so iterating over each item in list
            for dollaramount in dollaramounts:
                #stripping out commas and $ signs
                dollaramount = int(dollaramount.replace(',', '').replace('$', ''))
                #adding dollar amount to allmonies list
                allmonies.append(dollaramount)
                
                #if the dollar amount is already in the dollar amount dict
                #tick up the count by one
                if dollaramount in moneydict:
                    moneydict[dollaramount] += 1
                #if the dollar amount isn't already in the dollar amount dict
                #create entry and set it to one
                if dollaramount not in moneydict:
                    moneydict[dollaramount] = 1


#create a new csv file to write out to           
outputfile = open('dollaramounts.csv', 'w')
csvwriter = csv.writer(outputfile)

#write out all mentions of moneies to a csv file, one amount per row
for money in allmonies:
    csvwriter.writerow([money])

#close the csv file    
outputfile.close()

#converting python list of giveaway amounts to an array to do binning/graphing
money = np.asarray(allmonies)

#some descriptive stats
print(np.amin(money))
print(np.amax(money))
print(np.std(money))

#creating a blank array for bins to bin data with
bins = np.array([])
y = 0

#creating a thousand bins
for counter in range (0,10000):
    #with a bin width of 25
    y += 25
    #appending bins to list
    bins = np.append(bins, y)


#putting data into bins
binneddata  = np.digitize(money, bins)

#creating an array with two rows, binned values and actual money values
combineddata = np.array([money, binneddata])

#saving binned data array to csv as row
np.savetxt("binnedcounts.csv", binneddata, delimiter=',')

#some descriptive stats of binned data
print(np.amin(binneddata))
print(np.amax(binneddata))
print(np.std(binneddata))

sns.distplot(binneddata)

## Let's see how well we can fit a parametric distribution to the data
##fit a parametric distribution to a dataset and visually evaluate how closely
##it corresponds to the observed data
sns.distplot(binneddata, kde=False, fit=stats.exponweib)
##fits well


sns.distplot(binneddata, kde=False, fit=stats.norm)
##fits terribly

##let's print the fit stats of the good fit
print(stats.exponweib.fit(binneddata))

##a problem with treating this data is the possibility of user bias
##that is, one user could share a lot of promotions, and that could overly
##skew the data, so let's create averages for each user to adjust for that.

##creating a dictionary where each user will be a key
userdict = {}

##creating a set to create a unique list of users
allusers = set()

##a quality control check to make sure we process all of the promotions
verifytotal = 0

for apost in masterdict:
    thepost = masterdict[apost]
    if float(thepost['apromotion']) > 0.5864:
        if '$' in thepost['text']:
            #only if there is a dollar amount in the text of the post
            dollaramounts = get_all_money_from_string(thepost['text'])
    
    
            ##if the user is already in the dict
            if thepost['fid'] in userdict:
                for dollaramount in dollaramounts:
                    if dollaramount != "$,":
                        verifytotal += 1
                        #stripping out commas and $ signs
                        cleandollaramount = int(dollaramount.replace(',', '').replace('$', ''))
                        binnedamount = np.digitize(cleandollaramount, bins)
                        #tick up correct binned amount
                        userdict[thepost['fid']][int(binnedamount)] +=1
            ##if the user is already in the dict    
            if thepost['fid'] not in userdict:
                ##populate the bins
                userdict[thepost['fid']] = {}
                for abin in range(0,10001):
                    userdict[thepost['fid']][abin] = 0
                #tick up appropriate bin
                for dollaramount in dollaramounts:
                    if dollaramount != "$,":
                        verifytotal += 1
                        #stripping out commas and $ signs
                        cleandollaramount = int(dollaramount.replace(',', '').replace('$', ''))
                        binnedamount = np.digitize(cleandollaramount, bins)
                        userdict[thepost['fid']][int(binnedamount)] +=1

#now lets create an average distribution across all users
averagedict = {}

##create bins
for abin in range(0,10001):
    ##empty list of scores
    averagedict[abin] = []

#put each users bin count in a list
for auser in userdict:
     for abin in range(0,10001):  
         averagedict[abin].append(userdict[auser][abin])

#let's get a final average for each bin         
finalaverages = {}
howmanyaveragetotal = 0
for listofscores in averagedict:
    finalaverages[listofscores] = np.mean(averagedict[listofscores])
    howmanyaveragetotal += sum(averagedict[listofscores])
    

##let's do a little analysis to see how many promotions we have of total as we
##go up in bin height

##first, we need a grand total average
grandtotal = 0
for abin in finalaverages:
    grandtotal += finalaverages[abin]

##make a dict to store the cumlative totals for each bin
cumulativetotal = {}

#to keep track of where we are
runningtotal = 0
for abin in finalaverages:
    runningtotal += finalaverages[abin]
    #store the results in the bin
    cumulativetotal[abin] = (runningtotal/grandtotal)*100

#let's dump the data   
outputfile = open('useraveraged.binnedby25.cumulativetotal.csv', 'w')
csvwriter = csv.writer(outputfile)

for abin in cumulativetotal:
    csvwriter.writerow([abin, cumulativetotal[abin]])
outputfile.close()

##let's use sets to see how many unique amounts there are in the data
uniqueamounts = set()

for apost in masterdict:
    thepost = masterdict[apost]
    if float(thepost['apromotion']) > 0.5864:
        if '$' in thepost['text']:
            #only if there is a dollar amount in the text of the post
            dollaramounts = get_all_money_from_string(thepost['text'])
            for dollaramount in dollaramounts:
                uniqueamounts.add(dollaramount)
                
print(len(uniqueamounts))
print(uniqueamounts)
