# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 08:56:44 2018

@author: sridh
"""

import pandas as pd
import numpy as np
import pandas
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import LassoLarsCV
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression

csvfile = 'finalmaster-ratios.csv'
alldata=pandas.read_csv(csvfile) 
print(alldata)

allvariablenames = list(alldata.columns.values)
newdata = alldata.drop(columns = ['# Purchases', 'B01001001', 'B01001002', 'B01001003', 'B01001004', 'B01001005', 'B01001006', 'B01001007' ] )

listofallpredictors = list(newdata.columns.values)

predictors = newdata[listofallpredictors]  
target = alldata['# Purchases']
                 
pred_train, pred_test, tar_train, tar_test = train_test_split(predictors, target, test_size=.3, random_state=123)

#myarray1 = np.asarray(pred_train)
#myarray2=np.asarray(tar_train,tar_test)
#X, y = make_regression(pred_train,tar_train)
model=LassoLarsCV(cv=10).fit(pred_train,tar_train)

predictors_model=pd.DataFrame(listofallpredictors)
#predictors_model.columns = ['label']
predictors_model['coeff'] = model.coef_

for index, row in predictors_model.iterrows():
    if row['coeff'] > 0:
        print(row.values)


train_error = mean_squared_error(tar_train, model.predict(pred_train))
print ('training data MSE')
print(train_error)

test_error=mean_squared_error(tar_test, model.predict(pred_test))
print ('testing data MSE')
print(test_error)

rsquared_train=model.score(pred_train,tar_train)
print ('training data R-square')
print(rsquared_train)


rsquared_test=model.score(pred_test,tar_test)
print ('testing data R-square')
print(rsquared_test)   

print("y interecept:")
print(model.intercept_)

             