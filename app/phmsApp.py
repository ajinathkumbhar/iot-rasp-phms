import os
from sensors.THSensor import THSensor
from sensors.MPU6050GyroAcc import MPU6050GryroAccSensor
from display.OledDisplay import OLEDDisplay
from sensors.SensorUtils import SensData
import sensors.pulse as pulse
from dashboard.ioAdafruitDash import ioAdafruitDash
import threading
import Queue
import time
import signal
import sys

THSens = THSensor()
GyroAcc = MPU6050GryroAccSensor()
Disp = OLEDDisplay()
dashboard = ioAdafruitDash()

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

def getGyroAccSensData():
    print 'Enter : getGyroAccSensData'
    dHT = {}
    while True :
        sensValues = GyroAcc.getData()
        #print ("main Gx=%.2f" %sensValues['Gx'], "Gy=%.2f" %sensValues['Gy'], "Gz=%.2f" %sensValues['Gz'])
        #print ("main Ax=%.2f" %sensValues['Ax'] , "Ay=%.2f" %sensValues['Ay'] , "Az=%.2f" %sensValues['Az'] )
        qGA.put(sensValues)
        time.sleep(.1)

def getHBSensData():
    print 'Enter : getHBSensData'
    q_pulse = Queue.Queue(maxsize=1)
    pulse_thread = threading.Thread(target=pulse.get_count, name='displaySensorData', args=(q_pulse,))
    lThreadsID.append(pulse_thread)
    pulse_thread.start()
    while True:
        if not q_pulse.empty():
            qHB.put(str(q_pulse.get()))
        time.sleep(.1)


def displaySensorData():
    print 'Enter : displaySensorData'
    while True:
        if qSensorData.empty():
            continue
        sd = qSensorData.get()
        Disp.showWithDefaultTheme(sd)
        time.sleep(.1)

def updateDashboard(sd):
    dashboard.update(sd)

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

def getSensorData(sd):
    print ' '
    print 'Enter : getSensorData'
    dTH = {}
    dGA = {}
    hbeat = None

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
        sd.temp = sd.temp
    if sd.humi is 0:
        sd.humi = sd.humi

    if sd.Gx is 0:
        sd.Gx = sd.Gx
    if sd.Gy is 0:
        sd.Gy = sd.Gy
    if sd.Gz is 0:
        sd.Gz = sd.Gz
    if sd.Ax is 0:
        sd.Ax = sd.Ax
    if sd.Ay is 0:
        sd.Ay = sd.Ay
    if sd.Az is 0:
        sd.Az = sd.Az
    if sd.hbeat is 0:
        sd.hbeat = sd.hbeat

    print 'Exit : getSensorData'

def init():
    dashboard.setupClient()
    dumpBoardInfo()
    Disp.setupDisplay()
    GyroAcc.setup()
    startSensorsThreads()

def captureSensorDataAndUpdateToDashboard():
    while True:
        sdCurrent = SensData()
        getSensorData(sdCurrent)
        qSensorData.put(sdCurrent)
        updateDashboard(sdCurrent)
        sdPrevious = sdCurrent
        time.sleep(8)

def main():
    print 'Enter : main'
    print '---start----'
    signal.signal(signal.SIGINT,signalHandler)
    init()
    captureSensorDataAndUpdateToDashboard()
    print 'Exit : main'




if __name__ == '__main__':
    main()
