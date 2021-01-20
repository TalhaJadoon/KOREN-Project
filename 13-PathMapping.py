#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 19:26:19 2020

@author: user
"""

from os import walk
import pandas as pd
import os
# =============================================================================
# read all files in the folder
# =============================================================================
path = "Adeel2021/"
readPath = path + "AdeelPathStatistic/"
writePath = path + "AddelPathAgregrate/"
import shutil
shutil.rmtree(writePath)
os.mkdir(writePath)

# read all file names in path

for (dirpath, dirnames, filenames) in walk(readPath):
    break
del (dirpath, dirnames)
filenames.sort(reverse=True)
# path file
paths = pd.read_csv(path + "AddelPathsFile.txt", sep=";", header=None, index_col=0, names=pd.Series(range(9)))
cols = ["node_id", "interface_id", "pkts", "drop", "bps"]

countIter = 0
for filename in filenames[:1]:
    if countIter % 1000 == 0:           # just for checking loop progress 
        print (countIter)
    countIter += 1
    df = pd.read_csv(readPath+filename, header=None)
    df.columns = cols
    for node_id, source_node in paths[:1].iterrows():
        # print (node_id," --- \n", source_node)
        srcNodedf = pd.DataFrame(columns=[0])
        for path in source_node:
            # print (path)
            pathStat = [0,0,0]
            for interface in path.split(","):
                # print (interface)
                stat = df.loc[(df["node_id"] == interface.split("_")[0]) & (df["interface_id"] == interface.split("_")[1]), ["pkts","drop","bps"]]
                pathStat[0] += stat.values.tolist()[0][0]
                pathStat[1] += stat.values.tolist()[0][1]
                pathStat[2] += stat.values.tolist()[0][2]
            temp = pd.DataFrame(pathStat)
            temp[0][2] = temp[0][2].round(decimals=2)
            srcNodedf = pd.concat([srcNodedf, temp])
        srcNodedf.T.to_csv(writePath+filename, mode="a", header=None, index=False)
                # pathStat.append(stat.values.tolist()[0])
                # print (stat)









