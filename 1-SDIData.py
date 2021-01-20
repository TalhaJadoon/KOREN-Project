#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 12:23:39 2020

@author: user
"""
# =============================================================================
# all Imports
# =============================================================================
import pandas as pd
import os
import os.path
import json
import datetime

# import and create Elastic client
from elasticsearch import Elasticsearch
elastic_client = Elasticsearch(hosts=["elastic:koren124@61.252.55.180:9200"])

# =============================================================================
# topology Information - IPSDN Controller
# =============================================================================
# these below lines are commented to stop the request from controller
# import requests
# topology1 = requests.get("http://203.255.250.35:8180/1.0/topology")
# topologyData = topology1.json()
# with open('/home/user/Documents/KOREN Python Code/topology.json', 'w') as fp:
#     json.dump(topologyData, fp)

with open('/home/user/Documents/KOREN Python Code/topology.json', 'r') as fp:
    topologyData = json.load(fp)
links = topologyData["network_topology"]["topology"]["link"]
#create links
allLink = { }
for link in links:
    key = link["source"]["node_id"]+link["source"]["interface"] 
    allLink[key] = link["destination"]
    key = link["destination"]["node_id"]+link["destination"]["interface"] 
    allLink[key] = link["source"]

fileData = pd.DataFrame.from_dict(allLink, orient='index')
fileData.to_csv("AdeelData1100Final/Topology/links.csv")

# =============================================================================
# FUNCTION
# =============================================================================

def findLink(src_node, src_interface):
    return allLink[src_node+src_interface]

def uniqueInterfaceName(node_id, interface_name):
    # print (node_id, interface_name)
    return node_id.split("-")[0][1] + interface_name.split("e")[1]

def unqiueTimeValue(timeString):
    date_Time = datetime.datetime.strptime(timeString.split("+")[0], "%Y-%m-%dT%H:%M:%S")
    return (date_Time - datetime.datetime.strptime("2020-01-01T12:00:00", "%Y-%m-%dT%H:%M:%S")).total_seconds()

# =============================================================================
# body structure for specific node
# =============================================================================
def updateBody():
    myBody = {
        "from": 0,
        "size": 3500,
        "query": {
            "match_all": {}
        },
        "sort": [
            {"timestamp": "desc"}
            ]
    }
    return myBody

# timeseries data, incase of timeout error, run this body
def updateErrorBody():
    myBody = {
        "from": 0,
        "size": 2500,
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "timestamp":{
                                "lte": "2020-10-19T10:15:26+00:00"
                                }
                            }
                        }
                    ]
                }           
        },
        "sort": [
            {"timestamp": "desc"}
            ]
    }
    return myBody

# =============================================================================
# function data extraction and file writing N record per file --- apply conditions at rows
# =============================================================================
def readANDwrite(data, rCount, myFileName, interfaces):
    reqAttributes = ["rx_drop_pps","rx_pps","tx_bps", "tx_packets", "rx_bps", "tx_dropped", 
                      "rx_packets", "tx_pps", "tx_bytes", "rx_dropped", "rx_bytes"]
    path = "/home/user/Documents/KOREN Python Code/Adeel Data/"
    
    records = []
    for row in data:
        if (row["_source"]["interface_name"] in interfaces[row["_source"]["node_id"]]):
            rCount += 1
            values = []
            values.append(unqiueTimeValue(row["_source"]["timestamp"]))
            # values.append(row["_source"]["node_id"])    
            # values.append(row["_source"]["interface_name"])
            # values.append(uniqueInterfaceName(row["_source"]["node_id"], row["_source"]["interface_name"]))
            # linkInfo = findLink(row["_source"]["node_id"], row["_source"]["interface_name"])
            # values.append(linkInfo["node_id"])
            # values.append(uniqueInterfaceName(linkInfo["node_id"], linkInfo["interface"]))
            for index, value in enumerate(row["_source"]["stats"]):
                if value in reqAttributes:
                    values.append(row["_source"]["stats"][value])
            records.append(values)
            # print (rCount)
            
            if (rCount % recordsPerFile == 0):
                records = pd.DataFrame(records)
                if (os.path.isfile(path+myFileName)):
                    # print (len(records), " rows added to existing file")
                    records.to_csv(path + myFileName, header=False, mode ="a", index=False)
                else:
                    # print (len(records), "rows added to new file")
                    # records.columns = ["timestamp"]+reqAttributes
                    records.to_csv(path + myFileName, header=False, index=False)
                # print ("New file name created # ", rCount/recordsPerFile)
                records = []
                myFileName = "SDI-P1-" + str(rCount/recordsPerFile) + ".csv"
    
    if len(records) != 0:
        records = pd.DataFrame(records)
        # records.columns = ["timestamp"]+reqAttributes
        records.to_csv(path + myFileName, header=False, mode="a", index=False)
        # print (rCount, len(records), " rows added to existing file")
    # print ("--- QUERY RESULT COMPLETED ---\n")
    # print("Current Time Stamp: ", records.iloc[0]["timestamp"])
    return rCount, myFileName, records

# =============================================================================
# MAIN function
# =============================================================================
import shutil
shutil.rmtree("/home/user/Documents/KOREN Python Code/Adeel Data/")
os.mkdir("/home/user/Documents/KOREN Python Code/Adeel Data/")
recordsPerFile = 500
nodes = ["P1-Seoul", "P2-Daejeon", "P3-Pangyo", "P4-Gwangju", "P5-Daegu"]
interfaces = dict.fromkeys(nodes)
# interfaces["P1-Seoul"]   = ["prs1e39","prs1e1","prs1e33","prs1e16","prs2e18"]
interfaces["P1-Seoul"]   = ["prs1e39","prs1e1","prs1e33"] # prs1e16

# interfaces["P2-Daejeon"] = ["prs1e39","prs1e33","prs1e2","prs1e11","prs1e13","prs1e14"]
interfaces["P2-Daejeon"] = ["prs1e33","prs1e2","prs1e11","prs1e13","prs1e14"] # prs1e39

# interfaces["P3-Pangyo"]  = ["prs2e1","prs2e2","prs1e33","prs1e39"]
interfaces["P3-Pangyo"]  = ["prs2e2","prs1e33","prs1e39"]

# interfaces["P4-Gwangju"] = ["prs1e1","prs1e18","prs2e18"]
interfaces["P4-Gwangju"] = ["prs1e1"]

interfaces["P5-Daegu"]   = ["prs2e1","prs1e1"]

query_result = elastic_client.search(
    index = "kulcloud_node_interface_resource", 
    body = updateErrorBody(),
    scroll = '25s'   # time value for search
)
return_ls = readANDwrite(query_result["hits"]["hits"],0, "SDI-P1-0.0.csv", interfaces)
print ("Time taken: ", (query_result['took']/1000), "sec")

for i in range(4000):
    # print ("Query", i+1)
    query_result = elastic_client.scroll(
        scroll_id=query_result['_scroll_id'], 
        scroll='25s'
        )         # old scroll may be retured each time 
    # result1 = readANDwrite(query_result, nodeName+"-part-"+str(i+1)+".csv")
    return_ls = readANDwrite(query_result['hits']['hits'], return_ls[0], return_ls[1], interfaces)
    if (i%10 == 0):
        print (i+1, "Time taken: ", (query_result['took']/1000), "sec")

# '2020-10-20T09:50:00+00:00'
# '2020-10-20T01:36:24+00:00'
query_result["hits"]["hits"][len(query_result)-1]["_source"]["timestamp"]

# =============================================================================
# 123456789
# =============================================================================










