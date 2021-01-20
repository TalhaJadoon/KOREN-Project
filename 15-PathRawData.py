#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 00:13:01 2020

@author: user
"""

import pandas as pd
import os
# import csv
# =============================================================================
# read all files in the folder
# =============================================================================
path = "Adeel2021/"
readPath = path + "AdeelPathAggregrateSingleFile/"
writePath = path + "AdeelPathAggregrateFinal/"
import shutil
shutil.rmtree(writePath)
os.mkdir(writePath)

data = pd.read_csv(readPath+"Data.csv", header=None)
data = data.fillna(0)
dataHead = data.head(50)

# min and max function
minm = data.min(axis=0)
maxm = data.max(axis=0)
rang = maxm - minm

colCount = int(data.shape[1]/4 - 1)
# create cols names
colNames = []
for i in range(colCount):
    if i == 0:
        colNames.append("Agg"+str(i))
        colNames.append("Agg"+str(i+1))
        colNames.append("Agg"+str(i+2))
        colNames.append("Agg"+str(i+3))
    colNames.append("PKTS"+str(i))
    colNames.append("DROP"+str(i))
    colNames.append("BWD"+str(i))
    colNames.append("TIME"+str(i))
# assign col names to data
data.columns = colNames
dataHead.columns = colNames

# drop aggregrator cols from data
dataAggr = data[["Agg0", "Agg1", "Agg2", "Agg3"]].copy()
data = data.drop(columns=["Agg0", "Agg1", "Agg2", "Agg3"])
dataHead = data.head(50)

# list of column names to be normalized
colNormlize = []
for i in range(colCount):
    colNormlize.append("PKTS"+str(i))

# normalized here
from sklearn import preprocessing
x = data[colNormlize].values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
data[colNormlize] = pd.DataFrame(x_scaled, columns=data[colNormlize].columns)

data1 = data
# add aggregrater with normalized data 
for i in range(len(dataAggr.columns)):
    data1.insert(i,"Agg"+str(i),dataAggr["Agg"+str(i)])
data1Head = data1.head(50)

# add seprators and them merge seprators
for i in range(colCount):            
    index = data1.columns.get_loc("PKTS"+str(i))
    # data1.insert(index, "SEMI"+str(i), ";")
    if i % 9 == 0:
        data1.insert(index, "SEP3-"+str(i), -1)
        data1.insert(index, "SEP2-"+str(i), -1)
        data1.insert(index, "SEP1-"+str(i), 0)
        data1.insert(index, "SEP0-"+str(i), 0)
        data1["PKTS"+str(i)] = data1["SEP3-"+str(i)].map(str) + ";" + data1["PKTS"+str(i)].map(str)
        data1 = data1.drop(columns =["SEP3-"+str(i)])
        if i != 0:
            data1["TIME"+str(i-1)] = data1["TIME"+str(i-1)].map(str) +";" + data1["SEP0-"+str(i)].map(str)
            data1 = data1.drop(columns=["SEP0-"+str(i)])
    else:
        data1["TIME"+str(i-1)] = data1["TIME"+str(i-1)].map(str) + ";" + data1["PKTS"+str(i)].map(str)
        data1 = data1.drop(columns=["PKTS"+str(i)])
    if i == 0:
        data1["Agg3"] = data1["Agg3"].map(str) + "~" + data1["SEP0-0"].map(str)
        data1 = data1.drop(columns=["SEP0-0"])
        # data1.insert(index, "SEMI"+str(i), ";")
data1Head = data1.head(50)

# add seperatar ; at the end of row
data1[data1.columns[-1]] = data1[data1.columns[-1]].map(str) + ";"
data1Head = data1.head(50)

for i in range(0, len(data1),500):
    data1[i:i+500].to_csv( writePath+"Data"+str(round(i/500,0))+".txt", header=False, index = False)































