import os
from sensors.THSensor import THSensor
from sensors.OledDisplay import OLEDDisplay 
import threading

THSens = THSensor()
Disp = OLEDDisplay()

humidity=
temp=


def dumpBoardInfo():
    print '----------------------'
    print '1. ' + THSens.getSensorName()
    print '----------------------'

def getTHSensData():
    humidity, temperature = THSens.getTHdata()
    print('main Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
   
def getGyroAccSensData():
    print 'GryroAcc data ' + str(53)

def getHBSensData():
    print 'HBdata  ' + str(24)
    
def getSensorsData():
    THThread = threading.Thread(target=getTHSensData, name='getTHSensData')
    GyroAccThread = threading.Thread(target=getGyroAccSensData, name='getGyroAccSensData')
    HBThread = threading.Thread(target=getHBSensData, name='getHBSensData')
    THThread.start()
    GyroAccThread.start()
    HBThread.start()

    GyroAccThread.join()
    HBThread.join()
    THThread.join()
    
def main():
    print '---start----'
    dumpBoardInfo()
    Disp.setupDisplay()
    #Disp.testDisplay()
    getSensorsData()



    

if __name__ == '__main__':
    main()
