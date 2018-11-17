import os
from sensors.THSensor import THSensor
from sensors.OledDisplay import OLEDDisplay 

THSens = THSensor()
Disp = OLEDDisplay()

def dumpBoardInfo():
    print '----------------------'
    print '1. ' + THSens.getSensorName()
    print '----------------------'

def main():
    print '---start----'
    dumpBoardInfo()
    Disp.setupDisplay()
    Disp.testDisplay();

if __name__ == '__main__':
    main()
