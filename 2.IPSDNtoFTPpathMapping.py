#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 19:26:19 2020

@author: user
"""

# from os import walk
import pandas as pd
# import os
import csv
# =============================================================================
# read all files in the folder
# =============================================================================
readPath = "IPSDNrealTimeData/"
writePath = "IPSDNrealTimeData/"

paths = pd.read_csv("AddelPathsFile.txt", sep=";", header=None, index_col=0, names=pd.Series(range(9)))
cols = ["node_id", "interface_id","pkts","drop","bps"]
df = pd.read_csv(readPath+"realData.csv", header=None, index_col=0)
# df = df.drop(columns = ["index"])
df.columns = cols

pathdf = pd.DataFrame()
for node_id, source_node in paths[::-1].iterrows():
    print (node_id)
    for path in source_node[::-1]:
        print (path)
        pathdf.insert(0, path, [0,0,0,0])
        for link in path.split(","):
            pathdf[path] += df[link]
            # print (link)

# calaculate aggregration
aggrgrate = pathdf.sum(axis=1)

# normalized here
from sklearn import preprocessing
x = pathdf.values #returns a numpy array
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
data1 = pd.DataFrame(x_scaled, columns=pathdf.columns)

# add aggreration
data1.insert(0, "aggre", list(aggrgrate))
data2 = data1.values.flatten("F").tolist()

# create and open object for writing
csvFile = open(writePath + "realDataPaths.csv","w")
fObj = csv.writer(csvFile)
fObj.writerow(data2)
csvFile.close()

# data1.to_csv(writePath + "realDataPaths.csv", index=False, header=False)















