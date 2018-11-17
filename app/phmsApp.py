import os
from sensors.THSensor import THSensor

THSens = THSensor() 

def dumpBoardInfo():
    print '----------------------'
    print '1. ' + THSens.getSensorName()
    print '----------------------'

def main():
    print '---start----'
    dumpBoardInfo()



if __name__ == '__main__':
    main()
