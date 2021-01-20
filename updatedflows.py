#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 01:10:33 2020

@author: ncl
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 20:34:16 2020

@author: ncl
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 19:00:43 2020

@author: ncl
"""

from flask import Flask
app = Flask(__name__)

from dijkstra import Graph, DijkstraSPF
from dijkstra.dijkstra import AbstractDijkstraSPF

import mysql.connector
import json
import requests



#!/ db insertion test



#! Path from src to destination node

def pathfrom(clientname,providername):
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    
    Nodesx=[]

    db3.execute("SELECT NodeName FROM nodes")   
    for x in db3:
        Nodesx.append(x)
                    #!print(Nodesx)   
                    
                
                
    graph=Graph()
    for x in Nodesx:
        db3.execute ("SELECT SecondNodeName FROM Links where FirstNodeName = %s", x)
        for y in db3:
            graph.add_edge(x, y, 10)
            
#!    Nodesy=Nodesx            



    for src in Nodesx:
#            print("Check Point11111.....")            
            dijkstra=DijkstraSPF(graph,src)
#!            print(d , clientname) 
            if(src==clientname):
                for des in Nodesx:
#                    print(".........Check Poi22222.....")
                    if(des==providername):
                        print("\n Distance  from Source", "%3s ---> Destination %3s is:  %3s" % (src, des, dijkstra.get_distance(des)))
                        print("->", "\n this is the path from", src, "to", des , "\n", dijkstra.get_path(des),"\n")
                        return dijkstra.get_path(des)
                    
                    
                    
#! Function to src node Nodes                            
def createflowsesrcNode(src,nextNode,intents):
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    
#    print("InsertinSource node flows... I am  Here")
    intentv=intents[0]
    nodename=src[0]
    second=nextNode[0]
    db.execute("SELECT HostPort FROM Nodes WHERE NodeName= %s", src)
    port=db.fetchone()
    srcinport=port[0]
    
    #! Second node port while we first node
    temp1 = f'(SELECT `outportFirstnode`  FROM `links` WHERE `FirstNodeName`= \'{nodename}\' AND  `SecondNodeName`=\'{second}\' )'
#    print(f"query:     {temp1}")
    db.execute(temp1)
#    db.execute("SELECT outportFirstnode FROM Links where SecondNodeName = %s", nextNode)
    port=db.fetchone()
    srcoutport=port[0]    
#    db.execute("INSERT INTO `deployedflows`(`inport`, `outport`, `NodeName`, `Intentid`) VALUES %s %s %s", srcinport,srcoutport,intentv)    
#     db.execute("Select ")   
    temp = f'INSERT INTO `deployedflow` ( `outport`, `inport`, `nodename`, `intentid`) VALUES ({srcoutport},  {srcinport}, \'{nodename}\', {intentv} )'
#    print(f"query:     {temp}")
#db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
    db.execute(temp)
    Koren_db.commit()
    
    
#!will Insert reverse flows    
    temp = f'INSERT INTO `deployedflow` ( `outport`, `inport`, `nodename`, `intentid`) VALUES ({srcinport},  {srcoutport}, \'{nodename}\', {intentv} )'
#    print(f"query:     {temp}")
#db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
    db.execute(temp)
    Koren_db.commit()
    
    
    
    
#! Function to add flowrules for intermediate node    
def createflowsNode(prevNode,src,nextNode,intents):
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    intentv=intents[0]
    first=prevNode[0]
    second=src[0]
    nexti=nextNode[0]
    #! Second node port while we first node
    temp1 = f'(SELECT `inportSecondNode`  FROM `links` WHERE `FirstNodeName`= \'{first}\' AND  `SecondNodeName`=\'{second}\' )'
#    print(f"query:     {temp1}")
    db.execute(temp1)
    inpor=db.fetchone()
    inport=inpor[0]
    
    temp1 = f'(SELECT `outportFirstNode`  FROM `links` WHERE `FirstNodeName`= \'{second}\' AND  `SecondNodeName`=\'{nexti}\' )'
#    print(f"query:     {temp1}")
    db.execute(temp1)
    outpor=db.fetchone()
    outport=outpor[0]
    temp = f'INSERT INTO `deployedflow` ( `outport`, `inport`, `nodename`, `intentid`) VALUES ({outport},  {inport}, \'{second}\', {intentv} )'
#    print(f"query:     {temp}")
#db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
    db.execute(temp)
    Koren_db.commit()
    
#!Will insert reverse flow    
    
    temp = f'INSERT INTO `deployedflow` ( `outport`, `inport`, `nodename`, `intentid`) VALUES ({inport},  {outport}, \'{second}\', {intentv} )'
#    print(f"query:     {temp}")
    #db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
    db.execute(temp)
    Koren_db.commit()    
    
#! Function to add flowrules for destination node    
def createflowsdestNode(prevNode,destNode,intents):
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    intentv=intents[0]
    db.execute("SELECT HostPort FROM Nodes WHERE NodeName= %s", destNode)
    outpor=db.fetchone()
    outport=outpor[0]
    first=prevNode[0]
    second=destNode[0]
    #! Second node port while we first node
    temp1 = f'(SELECT `inportSecondNode`  FROM `links` WHERE `FirstNodeName`= \'{first}\' AND  `SecondNodeName`=\'{second}\' )'
#    print(f"query:     {temp1}")
    db.execute(temp1)
    inpor=db.fetchone()
    inport=inpor[0]
    temp = f'INSERT INTO `deployedflow` ( `outport`, `inport`, `nodename`, `intentid`) VALUES ({outport},  {inport}, \'{second}\', {intentv} )'
#    print(f"query:     {temp}")
#db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
    db.execute(temp)
    Koren_db.commit()
    
 
#will insert reverseflows    
    temp = f'INSERT INTO `deployedflow` ( `outport`, `inport`, `nodename`, `intentid`) VALUES ({inport},  {outport}, \'{second}\', {intentv} )'
#    print(f"query:     {temp}")
    #db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
    db.execute(temp)
    Koren_db.commit()
   
    
    


def nextnode (node, path):
    t=0
    for u in path:
        if node==u:
            t=1
        elif t==1:
            return u
def prevnode (node, path):
    for p in path:
        if p!=node:
          t=p  
        else:
            return t
        

def insertflows(src, dest,path,IntentID):
    
        Koren_db= mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="catalog"
            )

        db= Koren_db.cursor(buffered=True)
        db3= Koren_db.cursor(buffered=True) 

        id1=IntentID[0]
        for i in path:
            if (i==src):
#                print("path first node...is ..", i)
                nextq=nextnode(i, path)
#                print("this is next..",nextq)
                createflowsesrcNode (i,nextnode(i, path),IntentID)
            elif (i==dest):         
#                print("path dest node...is ..", i)
                prev=prevnode(i,path)
#                print("this is prev..",prev)
                createflowsdestNode(prevnode(i,path), i, IntentID)
            else: 
#                print("path intermitate node...is ..", i)
                nextq=nextnode(i, path)
#                print("this is next..",nextq)
                
                prev=prevnode(i,path)
#                print("this is prev..",prev)
                createflowsNode(prevnode(i,path), i, nextnode(i, path), IntentID)
#!        db3.execute("UPDATE `intent` SET `status`=1 WHERE `Intentid`= %s",id1)
        db3.execute( "SELECT `servicename` FROM `intent` WHERE  `Intentid`= %s",IntentID )
        servicename1=db3.fetchone()
        servicename=servicename1[0]
        print(" servicename is ....", servicename)
        temp1 = f'UPDATE `service` SET `status`=1 WHERE `servicename`= \'{servicename}\''
#        print(f"query:     {temp1}")
        db3.execute(temp1)
        temp = f'UPDATE `intent` SET `status`=1 WHERE `Intentid`= {id1}'
#        print(f"query:     {temp}")
        db3.execute(temp)
        #db3.execute("INSERT INTO `deployedflows` (`inport`, `outport`, `STATUS`, `Response`, `NodeName`, `Intentid`)  VALUES (`%s`, `%s`, 0, null,`%s`, %d)"% (  srcinport, srcoutport, nodename, intentv   ))
#!        db.execute(temp)
        
        Koren_db.commit()
 
flag= None

def calculatePath():
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    intentId=[]
    zero=0
    #! Fetching of intent ID from database
    temp=f'SELECT `Intentid`  FROM `intent` WHERE `status`= {zero}'
    db.execute( temp)       
    #!Excuting intents
    for inc in db:
        intentId.append(inc)
        
    for inloop in intentId:    
        print(inloop)
        inloop1=inloop[0]
        #1inloopa=inloop1[0]
        print("...........this intent..........!!!!!!!!\n\n\n", inloop1)
        #! Fetching service names for each intent
        db3.execute( "SELECT `servicename` FROM `intent` WHERE  `Intentid`= %s",inloop )
        for l in db3:
                servicename=l
                #! Fetching Provider nodname based on service name        
        db3.execute( "SELECT `ProviderNodeName` FROM `service` WHERE  `servicename`= %s",servicename)
        for f in db3:
            providername=f
#            print(f)
                    #! Fetching of VLAN based on IntendID name            

        qos=f'SELECT `QoSType`  FROM `intent` WHERE `Intentid`= {inloop1}'
        db3.execute(qos)
        qosu=db3.fetchall()
#        print(qosu)
        qosa=qosu[0]
        vL=f'SELECT `vLANid`  FROM `service` WHERE `servicename`= \'{servicename[0]}\''
#        print(f"quer: {vL}")
        db3.execute(vL)
        vLANID=db3.fetchone()
#        print(vLANID)
        vvv=vLANID[0]    
        vLv=f'SELECT `vLAN`FROM `vlans` WHERE `vLANid`=\'{vvv}\''
#        print(f"quer: {vLv}")
        db3.execute(vLv)
        VLAN=db3.fetchall()
        print("This is the VLan ID : ",VLAN)  
            
            
#! Fetching of Clientname based on clientname            
        db3.execute( "SELECT `ClientNodeName` FROM `Intent` WHERE  `Intentid`= %s",inloop)
        for u in db3:
            clientname=u
#            print(u)
        if(flag):
            print("*****Fetching Paths from ML*****")
        else:    
            path=pathfrom(clientname, providername)
            print("\n\n\n Best path from", clientname, " to ", providername, " is : " ,path)
        insertflows(clientname, providername, path, inloop)
#!        print("reverse, path")
#!        pathfrom( providername,clientname) 




itr=0
#!Deploying single flow having IntentID, Flow ID and vLANid
def deployflow(intentid,flowid,vLANID):
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    flow=flowid[0]
    intent=intentid[0]
    temp1 = f'(SELECT `inport`  FROM `deployedflow` WHERE `flowId`= {flow} AND `intentid`= {intent})'
#    print(f"query:     {temp1}")
    db3.execute(temp1)
    inport=db3.fetchall()
    inporte=inport[0]
    temp2 = f'(SELECT `outport`  FROM `deployedflow` WHERE `flowId`= {flow} AND `intentid`= {intent})'
#    print(f"query:     {temp2}")
    db3.execute(temp2)
    outport=db3.fetchall()
    outporte=outport[0]
    temp3 = f'(SELECT `nodename`  FROM `deployedflow` WHERE `flowId`= {flow} AND `intentid`= {intent})'
#    print(f"query:     {temp3}")
    db3.execute(temp3)
    nodename1=db3.fetchall()
    nodename=nodename1[0]
    print("Nodename : ", nodename)
    temp4a = f'(SELECT `servicename`  FROM `intent` WHERE `Intentid`= {intent})'
#    print(f"query:     {temp4a}")
    db3.execute(temp4a)
    servicename1=db3.fetchall()
    servicename=servicename1[0]
    
    temp5 = f'(SELECT `QoSType`  FROM `intent` WHERE `Intentid`= {intent})'
#    print(f"query:     {temp5}")
    db3.execute(temp5)
    qos1=db3.fetchone()
    qos=qos1[0]
    
    temp4 = f'(SELECT `Intentid`  FROM `intent` WHERE `servicename`= \'{servicename[0]}\' AND `QoSType`= \'{qos}\' AND`status`>= \'9\')'
#    print(f"query:     {temp4}")
    db3.execute(temp4)
    sameintent=db3.fetchone()
    if(sameintent):
        for i in sameintent:
            flowcheck = f'(SELECT `outport`, `inport`  FROM `deployedflow` WHERE `intentid`= {sameintent[0]} AND `nodename`= {nodename[0]})'
#            print(f"query:     {flowcheck}")
            db3.execute(flowcheck)
            previntentflow=db3.fetchone()
            flowcheck2 = f'(SELECT `outport`, `inport`  FROM `deployedflow` WHERE `intentid`= {intent} AND `nodename`= {nodename[0]})'
#            print(f"query:     {flowcheck2}")
            db3.execute(flowcheck2)
            currentintent=db3.fetchone()
            if(previntentflow==currentintent):
                Response= f'(SELECT `rapiesponse`  FROM `deployedflow` WHERE `intentid`= {sameintent[0]} AND `nodename`= {nodename[0]})'
#                print(f"query:     {Response}")
                db3.execute(Response)
                respons=db3.fetchall()
                response=respons[0]
                updateflow=f'(UPDATE `deployedflow` SET `status`= 3, `rapiesponse`= {response} WHERE `flowId`= {flow})'
                db3.execute(updateflow)
                Koren_db.commit()
                
    else:
        controller = f'(SELECT `ControllerIP`  FROM `nodes` WHERE `NodeName`= \'{nodename[0]}\')'
#        print(f"query:     {controller}")
        db3.execute(controller)
        controllerI=db3.fetchall()
        controllerIP=controllerI[0]
        
        swit = f'(SELECT `switchID`  FROM `nodes` WHERE `NodeName`= \'{nodename[0]}\')'
#        print(f"query:     {swit}")
        db3.execute(swit)
        switc=db3.fetchall()
        switch=switc[0]
        print("Switch ID, Controller IP", switch, controllerIP)
        
        prio=f'(SELECT `priority`  FROM `qos` WHERE `QoSType`= \'{qos}\')'
        db3.execute(prio)
        prior=db3.fetchall()
        priority=prior[0]
#        print("this is priority ",prior, "...", priority)
        
        vLv=f'(SELECT `vLAN` FROM `vlans` WHERE `vLANid`=\'{vLANID[0]}\')'
#        print(f"query:     {vLv}")
        db3.execute(vLv)
        VLAnV=db3.fetchall()
        vLANValue=VLAnV[0]
        respons=APIintegration(controllerIP[0], switch[0], vLANValue[0], priority[0], inporte[0], outporte[0])
        print(respons)
        updateflow=f'UPDATE `deployedflow` SET `status`= 2, `rapiesponse`= {respons} WHERE `flowId`= {flow}'
#        print(f"quer: {updateflow}")
        db3.execute(updateflow)
        Koren_db.commit()


        

def APIintegration(ctrIP,switchID,vLan,pri,inport,outport):
    URL=f'http://{ctrIP}:8181/1.0/flowtable/{switchID}/flow'
    #!res=(URL,generatebody(vLan, pri, inport, outport))
    print("Generated URL: ", URL)
    res=requests.post(url=URL,data=generatebody(vLan, pri, inport, outport))
    return res.text.split(":")[1][1:-1]

def generatebody(vlan,pri,inport,outport):
     
    Body1=f"{{\"dl_vlan\": \"{vlan}\", \"in_port\": \"{inport}\", \"table_id\": \"60\", \"priority\": \"{pri}\", \"instructions\": [{{\"instruction\": \"WRITE_ACTIONS\", \"actions\": [{{\"action\": \"OUTPUT\", \"value\": \"{outport}\"}}]}}]}}"
    print("Generated Body: ", Body1)
    return Body1    

#!Deployingflowrules for that aare only reserved
def deployflows():
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    print("Lets start deploying the flow rules")
#1    Fetching Intent Id having no flow Installed

    db.execute( "SELECT `Intentid` FROM `intent` WHERE `status`= 1 ")
    intents=db.fetchall()
    for i in intents:
        db3.execute( "SELECT `servicename` FROM `intent` WHERE  `Intentid`= %s",i )
        servicename=db3.fetchone()
        print("This is the Servicename: ",servicename)
        
        qos=f'(SELECT `QoSType`  FROM `intent` WHERE `Intentid`= \'{i[0]}\')'
#        print(f"query:     {qos}")

        db3.execute(qos)
        qosu=db3.fetchall()
        qosa=qosu[0]
        
        vL=f'(SELECT `vLANid`  FROM `service` WHERE `servicename`= \'{servicename[0]}\')'
#        print(f"query:     {vL}")

        db3.execute(vL)
        vLANID=db3.fetchone()
        print("vlanID is ..",vLANID)
        
        
        #Fetching alll flows having the intentid
        temp1 = f'(SELECT `flowId`  FROM `deployedflow` WHERE `intentid`= \'{i[0]}\' AND `status`= 0)'
#        print(f"query:     {temp1}")
        db3.execute(temp1)
        flowitr=db3.fetchall()
        for j in flowitr:
            deployflow(i,j,vLANID)
        temp = f'UPDATE `intent` SET `status`=2 WHERE `Intentid`= {i[0]}'
#        print(f"query:     {temp}")
        db3.execute(temp)
        Koren_db.commit()



def flowruledeletion(ctrIP,switchID,response):
    URL=f'http://{ctrIP}:8181/1.0/flowtable/{switchID}/flow/{response}'
    print(f"this is delete URL: {URL}")
    reds=requests.delete(url=URL)
    print("this is delet API response : ", reds)
#    return reds


        
def deletef(flow,ctr,switid):
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

    res1=f'(SELECT `rapiesponse` FROM `deployedflow` WHERE `flowId`= \'{flow}\')'
#    print(f"query:     {res1}")
    db3.execute(res1)
    respons=db3.fetchone()
#    print(respons)
    response=respons[0]
    
    
    flowruledeletion(ctr,switid,response)
#    reponse1=reponse.text.split(":")[1][1:-1]
    delflow=f'UPDATE `deployedflow` SET `status`= 5 WHERE `flowId`= {flow}'
    
#    print(f"quer: {delflow}")
    db3.execute(delflow)
    Koren_db.commit()
        
            
            
def deleteflows():
    
    print("Lets start the crashing of flows")
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

#    print("Lets start deploying the flow rules")
#1    Fetching Intent Id having no flow Installed

    db.execute( "SELECT `Intentid` FROM `intent` WHERE `status`= 2 ")
    intents=db.fetchall()
    for i in intents:
        
        #Fetching alll flows having the intentid
        temp1 = f'(SELECT `flowId`  FROM `deployedflow` WHERE `intentid`= \'{i[0]}\' AND `status`= 2)'
#        print(f"query:     {temp1}")
        db3.execute(temp1)
        flowitr=db3.fetchall()
        for j in flowitr:
            temp3 = f'(SELECT `nodename`  FROM `deployedflow` WHERE `flowId`= {j[0]} AND `intentid`= {i[0]})'
#            print(f"Nodenamequery:     {temp3}")
            db3.execute(temp3)
            nodename1=db3.fetchall()
            nodename=nodename1[0]
            controller = f'(SELECT `ControllerIP`  FROM `nodes` WHERE `NodeName`= \'{nodename[0]}\')'
#            print(f"ControllerIP query:     {controller}")
            db3.execute(controller)
            controllerI=db3.fetchall()
            controllerIP=controllerI[0]
        
            swit = f'(SELECT `switchID`  FROM `nodes` WHERE `NodeName`= \'{nodename[0]}\')'
#            print(f"SwitchID query:     {swit}")
            db3.execute(swit)
            switc=db3.fetchall()
            switch=switc[0]
#            print("Switch ID, value", switc,switch)
            deletef(j[0], controllerIP[0], switch[0])
        temp4 = f'(SELECT `servicename` FROM `intent` WHERE  `Intentid`=  {i[0]})'
#        print(f"Nodenamequery:     {temp4}")
        db3.execute(temp4)
        servicename1=db3.fetchone()
        servicename=servicename1[0]
#        print(" servicenameis ....", servicename)
        temp1 = f'UPDATE `service` SET `status`=0 WHERE `servicename`= \'{servicename}\''
#        print(f"query:     {temp1}")
        db3.execute(temp1)    
        temp = f'UPDATE `intent` SET `status`=3 WHERE `Intentid`= {i[0]}'
#        print(f"query:     {temp}")
        db3.execute(temp)
        Koren_db.commit()
    
            
def deleteflows1():
    
    print("Lets start the crashing of flows")
    
    Koren_db= mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="catalog"
        )

    db= Koren_db.cursor(buffered=True)
    db3= Koren_db.cursor(buffered=True) 

#    print("Lets start deploying the flow rules")
#1    Fetching Intent Id having no flow Installed

    db.execute( "SELECT `Intentid` FROM `intent` WHERE `status`= 5 ")
    intents=db.fetchall()
    for i in intents:
        
        #Fetching alll flows having the intentid
        temp1 = f'(SELECT `flowId`  FROM `deployedflow` WHERE `intentid`= \'{i[0]}\' AND `status`= 2)'
#        print(f"query:     {temp1}")
        db3.execute(temp1)
        flowitr=db3.fetchall()
        for j in flowitr:
            temp3 = f'(SELECT `nodename`  FROM `deployedflow` WHERE `flowId`= {j[0]} AND `intentid`= {i[0]})'
#            print(f"Nodenamequery:     {temp3}")
            db3.execute(temp3)
            nodename1=db3.fetchall()
            nodename=nodename1[0]
            controller = f'(SELECT `ControllerIP`  FROM `nodes` WHERE `NodeName`= \'{nodename[0]}\')'
#            print(f"ControllerIP query:     {controller}")
            db3.execute(controller)
            controllerI=db3.fetchall()
            controllerIP=controllerI[0]
        
            swit = f'(SELECT `switchID`  FROM `nodes` WHERE `NodeName`= \'{nodename[0]}\')'
#            print(f"SwitchID query:     {swit}")
            db3.execute(swit)
            switc=db3.fetchall()
            switch=switc[0]
#            print("Switch ID, value", switc,switch)
            deletef(j[0], controllerIP[0], switch[0])
        temp4 = f'(SELECT `servicename` FROM `intent` WHERE  `Intentid`=  {i[0]})'
#        print(f"Nodenamequery:     {temp4}")
        db3.execute(temp4)
        servicename1=db3.fetchone()
        servicename=servicename1[0]
#        print(" servicenameis ....", servicename)
        temp1 = f'UPDATE `service` SET `status`=0 WHERE `servicename`= \'{servicename}\''
#        print(f"query:     {temp1}")
        db3.execute(temp1)    
        temp = f'UPDATE `intent` SET `status`=3 WHERE `Intentid`= {i[0]}'
#        print(f"query:     {temp}")
        db3.execute(temp)
        Koren_db.commit()

@app.route('/InsertflowsDB')
def hello():
    calculatePath()
    print(".........!!!....")
    return "flowrules are generated!"

@app.route('/delete1')
def delete1():
    deleteflows1()
    print("All deleted")
    return "Mission oneDelete Successfull"



@app.route('/deleteall')
def delete():
    deleteflows()
    print("All deleted")
    return "Mission Delete Successfull"


@app.route('/sync')
def hello1():
    deployflows()
    print(".........After deploying flowrules!!!....")
    return "Synched!..."
if __name__ == '__main__':
    app.run()
    