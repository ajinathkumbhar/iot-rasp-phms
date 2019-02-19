import os
from sensors.THSensor import THSensor
from sensors.MPU6050GyroAcc import MPU6050GryroAccSensor
from display.OledDisplay import OLEDDisplay
from sensors.accevents import AccEvents
import sensors.event as evt
from sensors.SensorUtils import SensData
import sensors.pulse as pulse
from dashboard.ioAdafruitDash import ioAdafruitDash
import threading
import Queue
import time
import signal
import sys
from other import utils

THSens = THSensor()
GyroAcc = MPU6050GryroAccSensor()
Disp = OLEDDisplay()
dashboard = ioAdafruitDash()
mAccEvent = AccEvents()
mEvent = evt
# queue
qTH = Queue.Queue(maxsize=1)
qGA = Queue.Queue(maxsize=1)
qHB = Queue.Queue(maxsize=1)
qSensorData = Queue.Queue(maxsize=1)
qEvents = Queue.Queue(maxsize=10)
# thread list
lThreadsID = []

TAG = os.path.basename(__file__)

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

def acc_event_producer():
    while True:
        sens_val = GyroAcc.get_accelerometer_data()
        mAccEvent.detect_gesture_event(sens_val,qEvents)
        time.sleep(0.1)

def acc_event_consumer():
    while True:
        if not qEvents.empty():
            event = qEvents.get()
            if event == mEvent.GES_EVENT_FINGER_UP:
                utils.PLOGD(TAG,mAccEvent.get_event_str(event))

            if event == mEvent.GES_EVENT_FLIP:
                utils.PLOGD(TAG,mAccEvent.get_event_str(event))
        time.sleep(0.1)

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
    HBThread = threading.Thread(target=getHBSensData, name='getHBSensData')
    tAcc_producer = threading.Thread(target=acc_event_producer, name='acc_event')
    tAcc_consumer = threading.Thread(target=acc_event_consumer, name='acc_event_consumer')

    # Add threads id in list
    lThreadsID.append(DispThread)
    lThreadsID.append(THThread)
    lThreadsID.append(tAcc_consumer)
    lThreadsID.append(tAcc_producer)
    lThreadsID.append(HBThread)

    # start threads
    DispThread.start()
    THThread.start()
    HBThread.start()
    tAcc_producer.start()
    tAcc_consumer.start()

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

    if not qEvents.empty():
        event = qEvents.get()
        print "----------------- event : " + mAccEvent.get_event_str(event)

    if qHB.empty() is not True:
        hbeat = qHB.get()
        sd.hbeat = hbeat

    if sd.temp is 0:
        sd.temp = sd.temp
    if sd.humi is 0:
        sd.humi = sd.humi

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
