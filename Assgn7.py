# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 19:45:12 2018

@author: soham
"""

import pandas as pd
import json
import requests
csvfile = 'msas.csv'
msasdata=pd.read_csv(csvfile) 



tableids = ['B01001', 'B13016', 'B13017']

tableidstring = ','.join(tableids)

#Fetching Data from API
i=0
for i, row in msasdata.iterrows():
    
    requesturl = 'http://api.censusreporter.org/1.0/data/show/latest?table_ids=%s&geo_ids=31000US%s' % (tableidstring, row[0])
#Storing in json
loadedjson = requests.get(requesturl)
    #Loding json
a= loadedjson.json()