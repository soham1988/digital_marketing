#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 15:59:30 2018

@author: cvargo
"""

import pandas

#loading the control conversion data in
controlaudience = pandas.read_csv('controlaudience.csv')

#let's get the control audience mean and standard deviation
print('Control Mean:')
print(controlaudience['conversion'].mean())
print('Control Standard Deviation:')
print(controlaudience['conversion'].std())

#Now, let's use 2 standard deviation as our confidence intervals.
#Let's get those intervals
controllowerbound = controlaudience['conversion'].mean() - (controlaudience['conversion'].std()*2)
controlupperbound = controlaudience['conversion'].mean() + (controlaudience['conversion'].std()*2)

#Just printing the range
print('Control Range')
print('%s - %s' % (controllowerbound, controlupperbound))


#loading the test conversion data in
testaudience = pandas.read_csv('testaudience.csv')

#let's get the control audience mean and standard deviation
print('Test Mean:')
print(testaudience['conversion'].mean())
print('Test Standard Deviation:')
print(testaudience['conversion'].std())

#Now, let's use 2 standard deviation as our confidence intervals.
#Let's get those intervals
testlowerbound = testaudience['conversion'].mean() - (testaudience['conversion'].std()*2)

testupperbound = testaudience['conversion'].mean() + (testaudience['conversion'].std()*2)


#Just printing the range
print('Test Range')
print('%s - %s' % (testlowerbound, testupperbound))

#Is the highest end of our control range less than the lowest end of our
#test range?
print('Is %s greater than %s?' % (testlowerbound, controlupperbound))
print(testlowerbound > controlupperbound)