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

class SensData:
    def __init__(self):
        self.clear()
    def clear():
        self.temp = None
        self.humi = None
        self.Gx = None
        self.Gy = None
        self.Gz = None
        self.Ax = None
        self.Ay = None
        self.Az = None
        self.hbeat = None
    def getTemp():
        return self.temp
    def getHumidity():
        return self.humi
    def getGyroCoordinate():
        return self.Gx, Self.Gy, Self.Gz
    def getAccCoordinate():
        return self.Ax, Self.Ay, Self.Az

def signalHandler(sig,frame):
    print 'You pressed ctrl+c'
    THThread.stop()
    GyroAccThread.stop()
    HBThread.stop()
    sys.exit(0)

def dumpBoardInfo():
    print '----------------------'
    print '1. ' + THSens.getSensorName()
    print '----------------------'

def getTHSensData(qTH):
    dHT = {}
    while True :
        h, t = THSens.getTHdata()
        dHT['t'] = t
        dHT['h'] = h
        print('main Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(dHT['t'], dHT['h']))
        qTH.put(dHT)
    
def getGyroAccSensData(qGA):
    sensValues = GyroAcc.getData()
    print ("main Gx=%.2f" %sensValues['Gx'], "Gy=%.2f" %sensValues['Gy'], "Gz=%.2f" %sensValues['Gz'])
    print ("main Ax=%.2f" %sensValues['Ax'] , "Ay=%.2f" %sensValues['Ay'] , "Az=%.2f" %sensValues['Az'] )
    
def getHBSensData(qHB):
    print 'HBdata  ' + str(24)
    
def startSensorsThreads():
    THThread = threading.Thread(target=getTHSensData, name='getTHSensData', args=(qTH,))
    GyroAccThread = threading.Thread(target=getGyroAccSensData, name='getGyroAccSensData', args=(qGA,))
    HBThread = threading.Thread(target=getHBSensData, name='getHBSensData', args=(qHB,))
    THThread.start()
    GyroAccThread.start()
    HBThread.start()
    

def getSensorData():
    while True:
        if qTH.empty() is not True:
            print qTH.get()

    
def main():
    signal.signal(signal.SIGINT,signalHandler)
    print '---start----'
    dumpBoardInfo()
    Disp.setupDisplay()
    GyroAcc.setup()
    #Disp.testDisplay()
    startSensorsThreads()
    getSensorData()
    


if __name__ == '__main__':
    main()
