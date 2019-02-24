import os
from sensors.dht11 import THSensor
from sensors.mpu6050 import MPU6050GryroAccSensor
from display.oled_display import OLEDDisplay
from sensors.accevents import AccEvents
import sensors.event as evt
from sensors.sensor_utils import SensData
import sensors.pulse as pulse
from dashboard.io_adafruit import ioAdafruitDash
from sensors.alert import Alert
from other import utils
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
mAlert = Alert()
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
    utils.PLOGE(TAG,'You pressed ctrl+c')
    utils.PLOGE(TAG,lThreadsID)
    if len(lThreadsID) == 0:
        sys.exit(0)
    for threadId in lThreadsID:
        utils.PLOGE(TAG,'killing thread ' + str(threadId))
        threadId._Thread__stop()
    sys.exit(0)

def dumpBoardInfo():
    utils.PLOGD(TAG, "----------------------")
    utils.PLOGD(TAG, "1." + THSens.getSensorName())
    utils.PLOGD(TAG, "----------------------")

def getTHSensData():
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
    q_pulse = Queue.Queue(maxsize=1)
    pulse_thread = threading.Thread(target=pulse.get_count, name='displaySensorData', args=(q_pulse,))
    lThreadsID.append(pulse_thread)
    pulse_thread.start()
    while True:
        if not q_pulse.empty():
            qHB.put(str(q_pulse.get()))
        time.sleep(.1)


def displaySensorData():
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

def getSensorData(sdPre,sdCurr):
    if qTH.empty() is not True:
        dTH = qTH.get()
        sdCurr.temp = dTH['t']
        sdCurr.humi = dTH['h']

    if not qEvents.empty():
        event = qEvents.get()
        utils.PLOGD(TAG,"event : " + mAccEvent.get_event_str(event))
        sdCurr.acc_event = event

    if qHB.empty() is not True:
        hbeat = qHB.get()
        sdCurr.hbeat = hbeat

    if sdCurr.temp is 0:
        sdCurr.temp = sdPre.temp
    if sdCurr.humi is 0:
        sdCurr.humi = sdPre.humi

    if sdCurr.hbeat is 0:
        sdCurr.hbeat = sdPre.hbeat

def init():
    dashboard.setupClient()
    dumpBoardInfo()
    Disp.setupDisplay()
    GyroAcc.setup()
    startSensorsThreads()

def captureSensorDataAndUpdateToDashboard():
    start_time = time.time()
    sdPrevious = SensData()
    while True:
        sdCurrent = SensData()
        getSensorData(sdPrevious,sdCurrent)
        qSensorData.put(sdCurrent)
        current_time = time.time()
        diff_time = current_time - start_time
        if diff_time >= 8:
            updateDashboard(sdCurrent)
            start_time = current_time
        mAlert.check_and_trigger_alert(sdCurrent)
        sdPrevious = sdCurrent
        time.sleep(1)

def main():
    utils.PLOGD(TAG,'Enter : main')
    signal.signal(signal.SIGINT,signalHandler)
    init()
    captureSensorDataAndUpdateToDashboard()
    utils.PLOGD(TAG,'Exit : main')





if __name__ == '__main__':
    main()
