import os
from sensors.THSensor import THSensor
from sensors.MPU6050GyroAcc import MPU6050GryroAccSensor
from sensors.OledDisplay import OLEDDisplay
from sensors.SensorUtils import SensData
import threading
import Queue
import time
import signal
import sys
import random

THSens = THSensor()
GyroAcc = MPU6050GryroAccSensor()
Disp = OLEDDisplay()

# queue
qTH = Queue.Queue(maxsize=1)
qGA = Queue.Queue(maxsize=1)
qHB = Queue.Queue(maxsize=1)
qSensorData = Queue.Queue(maxsize=1)

# thread list
lThreadsID = []


def signalHandler(sig,frame):
    print 'You pressed ctrl+c'
    print lThreadsID
    if len(lThreadsID) == 0:
        sys.exit(0)
    for threadId in lThreadsID:
        print 'killing thread ' + str(threadId)
        threadId._Thread__stop()
    sys.exit(0)

def dumpBoardInfo():
    print '----------------------'
    print '1. ' + THSens.getSensorName()
    print '----------------------'

def getTHSensData():
    print 'Enter : getTHSensData'
    dHT = {}
    while True:
        h, t = THSens.getTHdata()
        dHT['t'] = t
        dHT['h'] = h
        #print('main Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(dHT['t'], dHT['h']))
        qTH.put(dHT)

    print 'Exit : getTHSensData'

def getGyroAccSensData():
    print 'Enter : getGyroAccSensData'
    dHT = {}
    while True :
        sensValues = GyroAcc.getData()
        #print ("main Gx=%.2f" %sensValues['Gx'], "Gy=%.2f" %sensValues['Gy'], "Gz=%.2f" %sensValues['Gz'])
        #print ("main Ax=%.2f" %sensValues['Ax'] , "Ay=%.2f" %sensValues['Ay'] , "Az=%.2f" %sensValues['Az'] )
        qGA.put(sensValues)
        time.sleep(.1)
    print 'Exit : getGyroAccSensData'

def getHBSensData():
    print 'Enter : getHBSensData'
    while True :
        hbeats = str(random.randint(65,82))
        #print 'hbeats: ' + hbeats
        qHB.put(hbeats)
        time.sleep(.1)
    print 'Exit : getHBSensData'


def displaySensorData():
    print 'Enter : displaySensorData'
    while True:
        if qSensorData.empty():
            continue
        sd = qSensorData.get()
        Disp.showWithDefaultTheme(sd)
        time.sleep(.1)
    print 'Exit : displaySensorData'


def startSensorsThreads():
    # Create threads
    DispThread = threading.Thread(target=displaySensorData, name='displaySensorData')
    THThread = threading.Thread(target=getTHSensData, name='getTHSensData')
    GyroAccThread = threading.Thread(target=getGyroAccSensData, name='getGyroAccSensData')
    HBThread = threading.Thread(target=getHBSensData, name='getHBSensData')

    # Add threads id in list
    lThreadsID.append(DispThread)
    lThreadsID.append(THThread)
    lThreadsID.append(GyroAccThread)
    lThreadsID.append(HBThread)

    # start threads
    DispThread.start()
    THThread.start()
    GyroAccThread.start()
    HBThread.start()

def getSensorData():
    print ' '
    print 'Enter : getSensorData'
    dTH = {}
    dGA = {}
    hbeat = None
    sdPrevious = SensData()
    sdCurrent  = SensData()

    while True:
        sd = SensData()
        sdCurrent = sd
        if qTH.empty() is not True:
            dTH = qTH.get()
            sd.temp = dTH['t']
            sd.humi = dTH['h']
        if qGA.empty() is not True:
            dGA = qGA.get()
            sd.Gx = dGA['Gx']
            sd.Gy = dGA['Gy']
            sd.Gz = dGA['Gz']
            sd.Ax = dGA['Ax']
            sd.Ay = dGA['Ay']
            sd.Az = dGA['Az']
        if qHB.empty() is not True:
            hbeat = qHB.get()
            sd.hbeat = hbeat

        if sd.temp is 0:
            sd.temp = sdPrevious.temp
        if sd.humi is 0:
            sd.humi = sdPrevious.humi

        if sd.Gx is 0:
            sd.Gx = sdPrevious.Gx
        if sd.Gy is 0:
            sd.Gy = sdPrevious.Gy
        if sd.Gz is 0:
            sd.Gz = sdPrevious.Gz
        if sd.Ax is 0:
            sd.Ax = sdPrevious.Ax
        if sd.Ay is 0:
            sd.Ay = sdPrevious.Ay
        if sd.Az is 0:
            sd.Az = sdPrevious.Az
        if sd.hbeat is 0:
            sd.hbeat = sdPrevious.hbeat

        qSensorData.put(sd)
        sdPrevious = sd
        time.sleep(.1)
    print 'Exit : getSensorData'



def main():
    print 'Enter : main'

    signal.signal(signal.SIGINT,signalHandler)
    print '---start----'
    dumpBoardInfo()
    Disp.setupDisplay()
    #Disp.testDisplay()
    GyroAcc.setup()
    startSensorsThreads()
    getSensorData()
    print 'Exit : main'




if __name__ == '__main__':
    main()
