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


def readData(file):
    with open(file, 'r', encoding='utf8', errors='ignore') as dataFile:
        days = []
        hours = []
        secList = []
        for line in dataFile:
            splitLine = line.split(',')
            if(len(splitLine) == 8):
                
                timeInSys = splitLine[7].split(' ')[2].replace('\n','')
                secondsInSys = time.strptime(timeInSys,'%H:%M:%S')
                secondsInSys = datetime.timedelta(hours=secondsInSys.tm_hour,minutes=secondsInSys.tm_min,seconds=secondsInSys.tm_sec).total_seconds()
                day = splitLine[1].split(' ')[3];
                hour = splitLine[1].split(' ')[4].split(':')[0]

                days.append(day)
                hours.append(hour)
                secList.append(secondsInSys)
    return AvgWaitingData(days, hours, secList)

def AvgWaitingData(d,h,s):
    xAxis = []
    yAxis = []
    
    peopleCount = 0
    secSum = 0
    prevHr = 0
    prevDay = 27
    peopleCount = 0 
    
    i = 0
    
    for day in d:
        if(h[i] != prevHr):
            m, sec = divmod(secSum, 60)
            hr, m = divmod(m, 60)
            #print("Days: {},{}:00 In Que: {} Avg Wait: {}.{} hrs".format(prevDay, prevHr, peopleCount, int(hr),int(m)))
            try:
                xAxis.append(float("{}.{}".format(int(hr), int(m)))/peopleCount)
            except ZeroDivisionError:
                xAxis.append(float("{}.{}".format(int(hr), int(m))))
            yAxis.append(peopleCount)
            secSum = 0
            peopleCount = 0
            prevHr = h[i]    
            if (day != prevDay):
                prevDay = day
        secSum = secSum + s[i]
        peopleCount = peopleCount + 1
        i = i + 1    
    AVGWaitingTime = yAxis
    NumPeople= xAxis
    #return x,y
    return AVGWaitingTime, NumPeople


if __name__ == "__main__":
    print("Collecting data from files...")
    npX, npY = readData(npFile)
    pX, pY = readData(pFile)
    dpX, dpY = readData(dpFile)
    
    npX, npY = (list(x) for x in zip(*sorted(zip(npX, npY))))
    pX, pY = (list(x) for x in zip(*sorted(zip(pX, pY))))
    dpX, dpY = (list(x) for x in zip(*sorted(zip(dpX, dpY))))

 
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
        heigth = 900,
        showgrid = False,
        xaxis = dict(
            showgrid = False,
            title = "Number of People"
                ),
        yaxis = dict(
            showgrid = False,
            title = "Average Waiting Time(Hours)"
                ),
        legend=dict(
            y=0.5,
            traceorder='reversed',
            font=dict(
                size=12
            )
        )
    )
        
    fig = dict(data=data, layout=layout)
    py.image.save_as(fig, filename='AvgWait_2.png')
    print("Graph Completed.")