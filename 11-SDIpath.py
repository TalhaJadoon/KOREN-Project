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
# import os
# import os.path
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

with open('topology.json', 'r') as fp:
    topologyData = json.load(fp)
links = topologyData["network_topology"]["topology"]["link"]
#create links
allLink = { }
for link in links:
    key = link["source"]["node_id"]+link["source"]["interface"] 
    allLink[key] = link["destination"]
    key = link["destination"]["node_id"]+link["destination"]["interface"] 
    allLink[key] = link["source"]
    # linkdf = pd.DataFrame(allLink)
    # linkdf.to_json("allLinks.json")
# 
# fileData = pd.DataFrame.from_dict(allLink, orient='index')
# fileData.to_csv("AdeelPathFinal/Topology/links.csv")

# =============================================================================
# FUNCTION
# =============================================================================

# def findLink(src_node, src_interface):
#     return allLink[src_node+src_interface]

# def uniqueInterfaceName(node_id, interface_name):
#     # print (node_id, interface_name)
#     return node_id.split("-")[0][1] + interface_name.split("e")[1]

def unqiueTimeValue(timeString):
    date_Time = datetime.datetime.strptime(timeString.split("+")[0], "%Y-%m-%dT%H:%M:%S")
    return (date_Time - datetime.datetime.strptime("2020-11-01T12:00:00", "%Y-%m-%dT%H:%M:%S")).total_seconds()

# =============================================================================
# body structure for specific node
# =============================================================================
def updateBody():
    myBody = {
        "from": 0,
        "size": 2500,
        "query": {
            "match_all": { }
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
            "range": {
                "timestamp":{
                    "lte": lastErrorTime
                }
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
# ["rx_drop_pps","rx_pps","tx_pps","tx_bytes","rx_bytes"]
#      So if you look at
# "tx_bps" --> tx_byte accumulated value up to the present time ***
# "tx_bytes": --> bps of current tx ***
# "tx_pps": --> tx packet accumulation value up to the present time 
# "tx_packets" --> pps of current tx
# Likewise for rx
# "rx_bps": --> Accumulated value of rx_byte up to the present time
# "rx_bytes": --> bps of current rx
# "rx_pps": --> Packet accumulated value of rx up to the present time
# "rx_packets": --> pps of current rx
def readANDwrite(data):
    reqAttributes = ["rx_pps", "tx_dropped", "tx_pps", "tx_bytes", "rx_dropped", "rx_bytes"]
    records = []
    for row in data:
        if (row["_source"]["interface_name"] in interfaces[row["_source"]["node_id"]]):
            values = []
            # time = unqiueTimeValue(row["_source"]["timestamp"])
            # values.append(time)
            values.append(row["_source"]["node_id"])    
            values.append(row["_source"]["interface_name"])
            # values.append(uniqueInterfaceName(row["_source"]["node_id"], row["_source"]["interface_name"]))
            # linkInfo = findLink(row["_source"]["node_id"], row["_source"]["interface_name"])
            # values.append(linkInfo["node_id"])
            # values.append(uniqueInterfaceName(linkInfo["node_id"], linkInfo["interface"]))
            for index, value in enumerate(row["_source"]["stats"]):
                if value in reqAttributes:
                    values.append(row["_source"]["stats"][value])
            records.append(values)
            # print (rCount)
            records = pd.DataFrame(records)
            # fileName = row["_source"]["node_id"] + "_" + row["_source"]["interface_name"]
            records.to_csv(path + str(row["_source"]["timestamp"].split("+")[0][:-3]) + ".csv", mode="a", header=False, index=False)
            records = []
    return records

# =============================================================================
# MAIN function
# =============================================================================
path = "Adeel2021/AdeelPath/"
# import shutil
# shutil.rmtree(path)
# os.mkdir(path)
recordsPerFile = 5000
nodes = ["P1-Seoul", "P2-Daejeon", "P3-Pangyo", "P4-Gwangju", "P5-Daegu"]
interfaces = dict.fromkeys(nodes)
# interfaces["P1-Seoul"]   = ["prs1e39","prs1e1","prs1e33","prs1e16","prs2e18"]
interfaces["P1-Seoul"]   = ["prs1e39","prs1e1","prs1e33", "prs1e16","prs2e18"]

# interfaces["P2-Daejeon"] = ["prs1e39","prs1e33","prs1e2","prs1e11","prs1e13","prs1e14"]
interfaces["P2-Daejeon"] = ["prs1e33","prs1e2","prs1e11","prs1e13","prs1e14", "prs1e39", "prs1e12", "prs1e17"]

# interfaces["P3-Pangyo"]  = ["prs2e1","prs2e2","prs1e33","prs1e39"]
interfaces["P3-Pangyo"]  = ["prs1e33","prs1e39", "prs2e1","prs2e2"]

# interfaces["P4-Gwangju"] = ["prs1e1","prs1e18","prs2e18"]
interfaces["P4-Gwangju"] = ["prs1e1","prs1e18","prs2e18"]

interfaces["P5-Daegu"]   = ["prs1e1", "prs2e1"]

query_result = elastic_client.search(
    index = "kulcloud_node_interface_resource", 
    body = updateBody(),
    scroll = '25s'   # time value for search
)
return_ls = readANDwrite(query_result["hits"]["hits"])
print ("0 Time taken: ", (query_result['took']/1000), "sec")

for i in range(2500):
    # print ("Query", i+1)
    query_result = elastic_client.scroll(
        scroll_id=query_result['_scroll_id'], 
        scroll='25s'
        )         # old scroll may be retured each time 
    # result1 = readANDwrite(query_result, nodeName+"-part-"+str(i+1)+".csv")
    return_ls = readANDwrite(query_result['hits']['hits'])
    if (i%20 == 0):
        print (i+1, "Time taken: ", (query_result['took']/1000), "sec")

# '2020-10-20T09:50:00+00:00'
# '2020-10-20T01:36:24+00:00'
lastErrorTime = query_result["hits"]["hits"][len(query_result)-1]["_source"]["timestamp"]














