#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 13:57:54 2020

@author: user
"""
import json
import requests
import pandas as pd

controllerIP = "http://61.252.53.21:8180"
# topology1 = requests.get("http://61.252.53.21:8180/1.0/topology")
# topologyData = topology1.json()
# del(topology1)

# with open('/home/user/Documents/KOREN-Python-Code/topology.json', 'r') as fp:
#     topologyData = json.load(fp)
# nodesData = topologyData["network_topology"]["topology"]["node"]
# controllerIPs = []
# for nodes in nodesData:
#     controllerIPs.append(nodes["ipaddress"])

# Nodes names and interfaces
nodes = ["P1-Seoul", "P2-Daejeon", "P3-Pangyo", "P4-Gwangju", "P5-Daegu"]
interfaces = dict.fromkeys(nodes)
interfaces["P1-Seoul"]   = ["prs1e39","prs1e1","prs1e33", "prs1e16","prs2e18"]
interfaces["P2-Daejeon"] = ["prs1e33","prs1e2","prs1e11","prs1e13","prs1e14", "prs1e39", "prs1e12", "prs1e17"]
interfaces["P3-Pangyo"]  = ["prs1e33","prs1e39", "prs2e1","prs2e2"]
interfaces["P4-Gwangju"] = ["prs1e1","prs1e18","prs2e18"]
interfaces["P5-Daegu"]   = ["prs1e1", "prs2e1"]

dropCol = ['collisions', 'multicast', 'rx_bytes', 'rx_compressed', 'rx_crc_errors', 'rx_crc_pps', 'rx_drop_pps',
       'rx_error_pps', 'rx_errors', 'rx_fifo_errors', 'rx_frame_errors', 'rx_length_errors', 'rx_missed_errors', 'rx_over_errors', 
       'rx_pps', 'tx_aborted_errors', 'tx_bytes', 'tx_carrier_errors', 'tx_compressed', 'tx_errors',
       'tx_fifo_errors', 'tx_heartbeat_errors', 'tx_pps', 'tx_window_errors']

# idx = 0
# request = "http://203.255.250.35:8180/1.0/monitoring/traffic/node/"+nodes[idx]+"/interface/"+interfaces[nodes[idx]][0]
# Traffic data with node and interface name
df = pd.DataFrame(0, index=[0], columns=[0,1,2,3])          # tp 
for nodeName in interfaces:
    print (nodeName)
    for interfaceName in interfaces[nodeName]:
        request = controllerIP + "/1.0/monitoring/traffic/node/"+nodeName+"/interface/"+interfaceName
        # print (request)
        interfaceTraffic = json.loads(requests.get(request).text)
# create dataframe and save interface and drop column
        traffic = pd.DataFrame.from_dict(interfaceTraffic)
        traffic = traffic.rename(columns= {"stats": nodeName+"_"+traffic["interface_name"]["collisions"]})
        traffic = traffic.drop(columns=["interface_name"])
        traffic = traffic.drop(index=dropCol).T
# find pkts, drop, bwd, time and drop all other columns
        traffic.insert(0, 3, 60)
        traffic.insert(0, 2, traffic["rx_bps"] + traffic["tx_bps"])
        traffic.insert(0, 1, traffic["rx_dropped"] + traffic["tx_dropped"])
        traffic.insert(0, 0, traffic["rx_packets"] + traffic["tx_packets"])
        traffic = traffic.drop(columns=["rx_packets", "tx_packets", "rx_dropped","tx_dropped","rx_bps","tx_bps"])
        df = pd.concat([df, traffic]) # merge the dataframe by using list or by using ??? 
        # idx += 1    # used for column names
df = df.drop(index=[0])
df.to_csv("IPSDNrealTimeData/realData.csv", header = False)

# print(interfaceTraffic)


















