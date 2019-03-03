#!/usr/bin/env python

import os
from app.sensors.dht11 import THSensor
from app.sensors.mpu6050 import MPU6050GryroAccSensor
from app.display.oled_display import OLEDDisplay
from app.sensors.accevents import AccEvents
import app.sensors.event as evt
from app.sensors.sensor_utils import SensData
import app.sensors.pulse as pulse
from app.dashboard.io_adafruit import ioAdafruitDash
from app.sensors.alert import Alert
from app.other import utils
import threading
import Queue
import time
import signal
import sys

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
qEvents = Queue.Queue(maxsize=10)
# thread list
lThreadsID = []

TAG = os.path.basename(__file__)


def temp_humidity_data():
    dHT = {}
    while True:
        h, t = THSens.getTHdata()
        dHT['t'] = t
        dHT['h'] = h
        # print('main Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(dHT['t'], dHT['h']))
        qTH.put(dHT)


def acc_event_producer():
    GyroAcc.setup()
    while True:
        sens_val = GyroAcc.get_accelerometer_data()
        mAccEvent.detect_gesture_event(sens_val, qEvents)
        time.sleep(0.1)


def acc_event_consumer():
    while True:
        if not qEvents.empty():
            event = qEvents.get()
            if event[1] == mEvent.GES_EVENT_FINGER_UP:
                utils.PLOGD(TAG, mAccEvent.get_event_str(event[1]))

            if event[1] == mEvent.GES_EVENT_FLIP:
                utils.PLOGD(TAG, mAccEvent.get_event_str(event[1]))
        time.sleep(0.1)


def pulse_data():
    q_pulse = Queue.Queue(maxsize=1)
    pulse_thread = threading.Thread(target=pulse.get_count, name='displaySensorData', args=(q_pulse,))
    lThreadsID.append(pulse_thread)
    pulse_thread.start()
    while True:
        if not q_pulse.empty():
            qHB.put(str(q_pulse.get()))
        time.sleep(.1)



class PhmsCore(object):
    def __init__(self):
        self.name = "phmscore"

    def dumpBoardInfo(self):
        utils.PLOGD(TAG, "----------------------")
        utils.PLOGD(TAG, "1." + THSens.getSensorName())
        utils.PLOGD(TAG, "----------------------")

    def update_dashboard(self,sd):
        dashboard.update(sd)

    def startSensorsThreads(self):
        # Create threads
        THThread = threading.Thread(target=temp_humidity_data, name='getTHSensData')
        HBThread = threading.Thread(target=pulse_data, name='getHBSensData')
        tAcc_producer = threading.Thread(target=acc_event_producer, name='acc_event')
        tAcc_consumer = threading.Thread(target=acc_event_consumer, name='acc_event_consumer')

        # Add threads id in list
        lThreadsID.append(THThread)
        lThreadsID.append(tAcc_consumer)
        lThreadsID.append(tAcc_producer)
        lThreadsID.append(HBThread)

        # start threads
        THThread.start()
        HBThread.start()
        tAcc_producer.start()
        tAcc_consumer.start()

    def getSensorData(self,sdPre,sdCurr):
        if qTH.empty() is not True:
            dTH = qTH.get()
            sdCurr.temp = dTH['t']
            sdCurr.humi = dTH['h']

        # if not qEvents.empty():
        event = mAccEvent.get_last_event()
        utils.PLOGD(TAG,"event : " + str(event))
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

    def init(self):
        dashboard.setupClient()
        self.dumpBoardInfo()
        self.startSensorsThreads()

    def captureSensorDataAndUpdateToDashboard(self):
        start_time = time.time()
        sdPrevious = SensData()
        while True:
            sdCurrent = SensData()
            self.getSensorData(sdPrevious,sdCurrent)
            current_time = time.time()
            diff_time = current_time - start_time
            if diff_time >= 15:
                self.update_dashboard(sdCurrent)
                start_time = current_time
            mAlert.check_and_trigger_alert(sdCurrent)
            sdPrevious = sdCurrent
            time.sleep(1)

    def start_app(self):
        utils.PLOGD(TAG,'Enter : main')
        self.init()
        self.captureSensorDataAndUpdateToDashboard()
        utils.PLOGD(TAG,'Exit : main')


def signalHandler(sig,frame):
    utils.PLOGE(TAG,'You pressed ctrl+c')
    utils.PLOGE(TAG,lThreadsID)
    if len(lThreadsID) == 0:
        sys.exit(0)
    for threadId in lThreadsID:
        utils.PLOGE(TAG,'killing thread ' + str(threadId))
        threadId._Thread__stop()
    sys.exit(0)

phms_app = PhmsCore()

def main():
    signal.signal(signal.SIGINT,signalHandler)
    phms_app.start_app()

if __name__ == "__main__":
    main()
