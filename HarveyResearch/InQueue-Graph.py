# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np

#For PC
#pFile = 'F:/HarveyResearch/Graph_Data/AllOut_priority.txt'
#npFile = 'F:/HarveyResearch/Graph_Data/AllOut_no_priority.txt'
#dpFile = 'F:/HarveyResearch/Graph_Data/AllOut_dynamic_priority.txt'

#For Mac
pFile = '/Volumes/Buffalo/HarveyResearch/Graph_Data/AllOut_priority.txt'
npFile = '/Volumes/Buffalo/HarveyResearch/Graph_Data/AllOut_no_priority.txt'
dpFile = '/Volumes/Buffalo/HarveyResearch/Graph_Data/AllOut_dynamic_priority.txt'

py.sign_in('JStuve', 'mVRUE6CCF94yvNnRxeuu') # Replace the username, and API key with your credentials.


def InQueueData(file):
    days = [27,28,29,30,31]
    date = []
    count = np.zeros(len(days) * 24)
    for day in days:
        for h in range(0,24):
            if(str(day) == '31'):
                date.append("Sept 1, "+ str(h) + ":00")
            else:
                date.append("Aug " + str(day) + ", " + str(h) + ":00")
    
    with open(file, 'r', encoding='utf8', errors='ignore') as dataFile:
        for line in dataFile:
            splitLine = line.split(',')
            if(len(splitLine) == 8):
                timeInQueue = ''.join(splitLine[6].split(' ')[2].split(':'))
                if(int(timeInQueue) != 0):
                    dayArrived = splitLine[1].split(' ')[3]
                    hourArrived = splitLine[1].split(' ')[4].split(':')[0]
                    hoursInQueue = splitLine[6].split(' ')[2].split(':')[0]
                    
                    dateIndex = date.index("Aug " + dayArrived + ", " + str(int(hourArrived)) + ":00") #Index of hour person is in queue
                    count[dateIndex] = count[dateIndex] + 1
                    for extraHour in range(1, int(hoursInQueue)-1):
                        count[dateIndex + extraHour] = count[dateIndex + extraHour] + 1

    return date, count



if __name__ == "__main__":
    print("Collecting data from files...")
    npX, npY = InQueueData(npFile)
    pX, pY = InQueueData(pFile)
    dpX, dpY = InQueueData(dpFile)
    #InQueueData(pFile)
    #print(npX)
    #print(npY)
    
    #Create a trace for each readData() values above
    print("Creating plotly graphs...")
    traceP = go.Scatter(
        x=pX,
        y=pY,
        mode='lines',
        name="Priority",
        hoverinfo='Priority',
        line=dict(
            shape='hv'
        )
    )
    
    traceNP = go.Scatter(
        #x=["Aug 27, 0:00","Aug 27, 8:00","Aug 27, 17:00","Aug 28, 0:00","Aug 28, 8:00","Aug 28, 17:00", "Aug 29, 0:00", "Aug 29, 8:00","Aug 28, 17:00" ],
        x=npX,
        y=npY,
        mode='lines',
        name="FCFS",
        hoverinfo='FCFS',
        line=dict(
            shape='hv'
        )
    )
    
    traceDP = go.Scatter(
        #x=["Aug 27, 0:00","Aug 27, 8:00","Aug 27, 17:00","Aug 28, 0:00","Aug 28, 8:00","Aug 28, 17:00", "Aug 29, 0:00", "Aug 29, 8:00","Aug 28, 17:00" ],
        x=dpX,
        y=dpY,
        mode='lines',
        name="Hybrid Scheduling",
        hoverinfo='FCFS',
        line=dict(
            shape='hv'
        )
    )
        
    data = [traceNP, traceP, traceDP]
    
    layout = dict(
        width = 900,
        heigth = 900,
        xaxis = dict(
            title = "Time of Day",
            titlefont = dict(
                    size = 20,
                    color = "#000"
            ),
            tickfont = dict(
                    size = 14,
                    color = "#000"
            ),
            showgrid = False,
            range=[83,102],
            ticks='outside',
            dtick=4
        ),
        yaxis = dict(
            title = "Number of People in Queue",
            titlefont = dict(
                    size = 20,
                    color = "#000"
            ),
            tickfont = dict(
                    size = 14,
                    color = "#000"
            ),
            showgrid = False,
        ),
        legend=dict(
            y=0.5,
            traceorder='reversed',
            font=dict(
                size = 20,
                color = "#000"
            )
        )
    )
        
    fig = dict(data=data, layout=layout)
    py.image.save_as(fig, filename='InQue_6.png')
    print("Graph Completed.")