#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:08:31 2020

@author: user
"""

import pandas as pd
import os
# =============================================================================
# read all files in the folder
# =============================================================================
path = "Adeel2021/AdeelPath"
from os import walk
for (dirpath, dirnames, filenames) in walk(path):
    break
del (dirpath, dirnames)
# =============================================================================
# read previous csv and calculate aggregrate and save as single row
# =============================================================================
# if (not os.path.isfile(path+"Final")):
#     os.mkdir(path+"Final")
import shutil
shutil.rmtree(path+"Statistic/")
os.mkdir(path+"Statistic/")
filenames.sort(reverse=True)
cols = ["node_id", "interface_id","rx_pkts","tx_drop","tx_pkts","tx_bps","rx_drop","rx_bps"]
dropFileCount = 0
for idx, cFile in enumerate(filenames[:len(filenames)-1]):
    pastFile = filenames[idx+1]
    # print (idx, cFile, "---", pastFile)  
    
    cdf = pd.read_csv(path+"/"+cFile, header=None)
    pastdf = pd.read_csv(path+"/"+pastFile, header=None)
    cdf.columns = pastdf.columns = cols
    if len(cdf) == 22 and len(pastdf):
        cdf = cdf.sort_values(["node_id", "interface_id"]).reset_index()
        pastdf = pastdf.sort_values(["node_id", "interface_id"]).reset_index()
        
        cdf["pkts"] = (cdf["rx_pkts"] - pastdf["rx_pkts"]) + (cdf["tx_pkts"] - pastdf["tx_pkts"])
        cdf["drop"] = (cdf["rx_drop"] - pastdf["rx_drop"]) + (cdf["tx_drop"] - pastdf["tx_drop"])
        cdf["bps"] = (cdf["rx_bps"] + pastdf["rx_bps"])/1000000000 + (cdf["tx_bps"] + pastdf["tx_bps"])/1000000000
        cdf = cdf.drop(columns= cols[3:] + ["index"] + ["rx_pkts"])
        del (pastdf)
        cdf[:22].to_csv(path+"Statistic/"+ cFile, index=False, header=False)
    else:
        dropFileCount += 1
    if (idx%1000 == 0):
        print (idx)












