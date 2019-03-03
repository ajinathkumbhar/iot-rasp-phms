#!/usr/bin/env python

from app.display.oled_display import OLEDDisplay
import signal
import sys
import threading
import time

olddisplay = OLEDDisplay()
lThreadsID = []

def signal_handler(sig,frame):
    print 'You pressed ctrl+c'
    print lThreadsID
    if len(lThreadsID) == 0:
        sys.exit(0)
    for threadId in lThreadsID:
        print 'killing thread ' + str(threadId)
        threadId._Thread__stop()
    sys.exit(0)

def show_dev_info():
    while True:
        olddisplay.testDisplay()
        time.sleep(1)
        
def main():
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGABRT, signal_handler)

    dev_info = threading.Thread(target=show_dev_info)
    lThreadsID.append(dev_info)
    dev_info.start()
    dev_info.join()

if __name__ == '__main__':
    main()