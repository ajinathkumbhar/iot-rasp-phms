import os
from sensors.THSensor import THSensor
from sensors.MPU6050GyroAcc import MPU6050GryroAccSensor
from sensors.OledDisplay import OLEDDisplay
import threading
import Queue
import time
import signal
import sys


THSens = THSensor()
GyroAcc = MPU6050GryroAccSensor()
Disp = OLEDDisplay()

# queue
qTH = Queue.Queue(maxsize=1)
qGA = Queue.Queue(maxsize=10)
qHB = Queue.Queue(maxsize=2)
qSensorData = Queue.Queue(maxsize=10)

# thread list
lThreadsID = []



class SensData:
    def __init__(self):
        self.clear()
    def clear(self):
        self.temp = None
        self.humi = None
        self.Gx = None
        self.Gy = None
        self.Gz = None
        self.Ax = None
        self.Ay = None
        self.Az = None
        self.hbeat = None
    def getTemp(self):
        return self.temp
    def getHumidity(self):
        return self.humi
    def getGyroCoordinate(self):
        return self.Gx, Self.Gy, Self.Gz
    def getAccCoordinate(self):
        return self.Ax, Self.Ay, Self.Az

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
        time.sleep(1)
    print 'Exit : getGyroAccSensData'

def getHBSensData():
    print 'Enter : getHBSensData'
    while True :
        hbeats = str(32)
        #print 'hbeats: ' + hbeats
        qHB.put(hbeats)
        time.sleep(1)
    print 'Exit : getHBSensData'


def displaySensorData():
    print 'Enter : displaySensorData'
    while True:
        if qSensorData.empty():
            continue
        sd = qSensorData.get()
        time.sleep(1)
        print 'temperature : ' + str(sd.temp)
        print 'humidity    : ' + str(sd.humi)
        print 'Gx          : ' + str(sd.Gx)
        print 'Gy          : ' + str(sd.Gy)
        print 'Gz          : ' + str(sd.Gz)
        print 'Ax          : ' + str(sd.Ax)
        print 'Ay          : ' + str(sd.Ay)
        print 'Az          : ' + str(sd.Az)
        print 'Pulses      : ' + str(sd.hbeat)
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
    while True:
        sd = SensData()
        if qTH.empty() is not True:
            dTH = qTH.get()
            #print dTH
            sd.temp = dTH['t']
            sd.humi = dTH['h']
        if qGA.empty() is not True:
            dGA = qGA.get()
            #print dGA
            sd.Gx = dGA['Gx']
            sd.Gy = dGA['Gy']
            sd.Gz = dGA['Gz']
            sd.Ax = dGA['Ax']
            sd.Ay = dGA['Ay']
            sd.Az = dGA['Az']
        if qHB.empty() is not True:
            hbeat = qHB.get()
            sd.hbeat = hbeat

        qSensorData.put(sd)
        time.sleep(1)
    print 'Exit : getSensorData'



def main():
    print 'Enter : main'

    signal.signal(signal.SIGINT,signalHandler)
    print '---start----'
    dumpBoardInfo()
    Disp.setupDisplay()
    GyroAcc.setup()
    #Disp.testDisplay()
    startSensorsThreads()
    getSensorData()
    print 'Exit : main'

if __name__ == '__main__':
    main()
