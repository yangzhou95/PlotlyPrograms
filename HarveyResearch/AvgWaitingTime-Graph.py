# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 15:03:27 2017

@author: jstuve
"""
import datetime
import time
import plotly.plotly as py
import plotly.graph_objs as go

#For PC
#pFile = 'F:/HarveyResearch/Graph_Data/AllOut_priority.txt'
#npFile = 'F:/HarveyResearch/Graph_Data/AllOut_no_priority.txt'

#For Mac
pFile = '/Volumes/Buffalo/HarveyResearch/Graph_Data/AllOut_priority.txt'
npFile = '/Volumes/Buffalo/HarveyResearch/Graph_Data/AllOut_no_priority.txt'
dpFile = '/Volumes/Buffalo/HarveyResearch/Graph_Data/AllOut_dynamic_priority.txt'

py.sign_in('JStuve', 'mVRUE6CCF94yvNnRxeuu') # Replace the username, and API key with your credentials.


def AvgWaitData(file):
    avgHour = [] 
    with open(file, 'r', encoding='utf8', errors='ignore') as dataFile:
        rescueeNumber = 0
        rescueeList = []
        secInQue = []
        for line in dataFile:
            splitLine = line.split(',')
            if(len(splitLine) == 8):
                
                timeInQue = splitLine[6].split(' ')[2].replace('\n','')
                secondsInQue = time.strptime(timeInQue,'%H:%M:%S')
                secondsInQue = datetime.timedelta(hours=secondsInQue.tm_hour,minutes=secondsInQue.tm_min,seconds=secondsInQue.tm_sec).total_seconds()

                rescueeNumber = rescueeNumber + 1
                rescueeList.append(rescueeNumber)
                secInQue.append(secondsInQue)
    
    
    for i in range(0, len(rescueeList)):
        s = sumRange(secInQue, 0, i)/rescueeList[i]
        m = s / 60
        h = m / 60
        avgHour.append(h)
        
#    print(rescueeList)
#    print(avgHour)
    return rescueeList, avgHour


def sumRange(List,startIndex,endIndex):                                                                                                                                                                                                
    sum = 0                                                                                                                                                                                                         
    for i in range(startIndex,endIndex+1,1):                                                                                                                                                                                        
        sum += List[i]                                                                                                                                                                                                  
    return sum


if __name__ == "__main__":
    print("Collecting data from files...")
    npX, npY = AvgWaitData(npFile)
    pX, pY = AvgWaitData(pFile)
    dpX, dpY = AvgWaitData(dpFile)
    
    #npX, npY = (list(x) for x in zip(*sorted(zip(npX, npY))))
    #pX, pY = (list(x) for x in zip(*sorted(zip(pX, pY))))
    #dpX, dpY = (list(x) for x in zip(*sorted(zip(dpX, dpY))))

 
    #Create a trace for each readData() values above
    print("Creating plotly graphs...")
    traceP = go.Scatter(
        x=pX,
        y=pY,
        mode='lines',
        name="Priority",
        hoverinfo='P',
    )
    
    traceNP = go.Scatter(
        x=npX,
        y=npY,
        mode='lines',
        name="Non-Priority",
        hoverinfo='NP',   
    )
    
    traceDP = go.Scatter(
        x=dpX,
        y=dpY,
        mode='lines',
        name="Dynamic Priority",
        hoverinfo='DP',   
    )
        
    data = [traceNP, traceP, traceDP]
    
    layout = dict(
        width = 900,
        heigth = 2000,
        showgrid = False,
        xaxis = dict(
            showgrid = False,
            title = "Number of People",
            titlefont = dict(
                    size = 18,
            ),
            tickfont = dict(
                    size = 18,
            ),
        ),
        yaxis = dict(
            showgrid = False,
            autosize = False,
            title = "Average Waiting Time(Hours)",
            titlefont = dict(
                    size = 18,
            ),
            tickfont = dict(
                    size = 18,
            ),
        ),
        legend=dict(
            y=0.5,
            traceorder='reversed',
            font=dict(
                size=16
            )
        )
    )
        
    fig = dict(data=data, layout=layout)
    py.image.save_as(fig, filename='AvgWait_3.png')
    print("Graph Completed.")