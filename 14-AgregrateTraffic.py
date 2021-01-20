#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 21:49:41 2020

@author: user
"""

from os import walk
import pandas as pd
import os
import csv
# =============================================================================
# read all files in the folder
# =============================================================================
path = "Adeel2021/"
readPath = path + "AdeelPathAgregrate/"
writePath = path + "AdeelPathAggregrateSingleFile/"
import shutil
shutil.rmtree(writePath)
os.mkdir(writePath)

# read all directioires
for (dirpath, dirnames, filenames) in walk(readPath):
    break
filenames.sort(reverse=True)

# generate col names
colNames = []
for i in range(9):      # 9 is calculate baesd on column count and divided by 3(pkts, drop, bandwidth)
    colNames.append("PKTS"+str(i))
    colNames.append("DROP"+str(i))
    colNames.append("BWD"+str(i))

# create and open object for writing
csvFile = open(writePath + "Data.csv","w")
fObj = csv.writer(csvFile)

for filename in filenames:
    df = pd.read_csv(readPath+filename, header=None)
    df.columns = colNames

# add time col in the data
    for colNo in range(9):
        index = df.columns.get_loc("BWD"+str(colNo))
        df.insert(index+1, "TIME"+str(colNo), 60)
    
    aggrdf = pd.DataFrame(columns=["PKTS","DROP","BWD","TIME"])
# aggregrate each col value
    for colNum in range(9):
        for colName in ["PKTS","DROP","BWD","TIME"]:
            if colNum == 0:
                aggrdf[colName] = df[colName+str(colNum)]
            else:
                aggrdf[colName] = aggrdf[colName] + df[colName+str(colNum)]

# aggregration of dataframe
    aggValues = list(aggrdf.sum(axis=0))
    aggValues[2] = round(aggValues[2],2)
    df = df.values.flatten("C").tolist()
    if aggValues[0] > 0 and aggValues[1] > 0 and aggValues[2] > 0:
        fObj.writerow(aggValues + df)
csvFile.close()






