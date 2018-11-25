import os
from sensors.THSensor import THSensor
from sensors.MPU6050GyroAcc import MPU6050GryroAccSensor
from sensors.OledDisplay import OLEDDisplay 
import threading

THSens = THSensor()
GyroAcc = MPU6050GryroAccSensor()
Disp = OLEDDisplay()

def dumpBoardInfo():
    print '----------------------'
    print '1. ' + THSens.getSensorName()
    print '----------------------'

def getTHSensData():
    humidity, temperature = THSens.getTHdata()
    print('main Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
   
def getGyroAccSensData():
    sensValues = GyroAcc.getData()
    print ("main Gx=%.2f" %sensValues['Gx'], "Gy=%.2f" %sensValues['Gy'], "Gz=%.2f" %sensValues['Gz'])
    print ("main Ax=%.2f" %sensValues['Ax'] , "Ay=%.2f" %sensValues['Ay'] , "Az=%.2f" %sensValues['Az'] )
    
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
    GyroAcc.setup()
    #Disp.testDisplay()
    getSensorsData()



    

if __name__ == '__main__':
    main()
