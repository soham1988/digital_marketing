    # -*- coding: utf-8 -*-
"""
Vargo in class data pivot and graphing
"""
import pandas

##this imports your graphing tool, seaborn as 'sns'
import seaborn as sns

##this assigns the filename we're trying to load in to a string variable
excelfile = 'nativeads.xls'

##this uses the pandas package to load the excel file into a pandas dataframe
adataframe = pandas.read_excel(excelfile)

#let's pivot the data like we did in excel
pivoteddata = adataframe.pivot_table(index='URL', aggfunc='mean')

##this graphs Cost and Conversions into a clean line plot with a simple
##regression analysis
sns.jointplot("Cost", "Conversions", data=pivoteddata, kind='reg')

##lets sort the data by cost from low to high
sorteddata = pivoteddata.sort_values("Cost")

##let's just take the 55 cheapest ads that we ran
firsthalf = sorteddata.head(55)

##let's see how that altered the strength of the correlation
sns.jointplot("Cost", "Conversions", data=firsthalf, kind='reg')

##what about the first 50?
firsthalf = sorteddata.head(50)

sns.jointplot("Cost", "Conversions", data=firsthalf, kind='reg')

##what about the last 55?
secondhalf = sorteddata.tail(55)

sns.jointplot("Cost", "Conversions", data=secondhalf, kind='reg')

##what about the last 50?
secondhalf = sorteddata.tail(50)

sns.jointplot("Cost", "Conversions", data=secondhalf, kind='reg')

secondhalf = sorteddata.tail(45)

sns.jointplot("Cost", "Conversions", data=secondhalf, kind='reg')

##let's get rid of the last one
secondhalfminusone = secondhalf.head(44)

sns.jointplot("Cost", "Conversions", data=secondhalfminusone, kind='reg')


##let's get rid of the last one
secondhalfminusone = secondhalf.head(30)

sns.jointplot("Cost", "Conversions", data=secondhalfminusone, kind='reg')