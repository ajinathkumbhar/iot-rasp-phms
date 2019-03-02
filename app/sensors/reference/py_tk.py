#!/usr/bin/env python

import Tkinter as tk
import time
import os
import threading
import signal
import sys

win = tk.Tk()
win.title("Phms")
win.overrideredirect(True)
win.geometry("480x320")
lThreadsID = []

stop_threads = False

start_button = tk.Button(win, text='Start', bg='bisque2', height=1, width=6)
start_button.grid(row=1, sticky=tk.NSEW)
exit_button = tk.Button(win, text='Exit', bg='bisque2', height=1, width=6)
exit_button.grid(row=2, sticky=tk.E)

def signalHandler(sig,frame):
    print 'You pressed ctrl+c'
    print lThreadsID
    if len(lThreadsID) == 0:
        sys.exit(0)
    for threadId in lThreadsID:
        print 'killing thread ' + str(threadId)
        threadId._Thread__stop()
    sys.exit(0)

def run_app():
    while True:
        print "Hey hello"
        time.sleep(1)

def start_app():
    app_thread = threading.Thread(target=run_app)
    lThreadsID.append(app_thread)
    app_thread.start()
    start_button.configure(state="disabled")

def exit_app():
    os.kill(os.getpid(), signal.SIGTERM)
    exit(0)

def main():
    signal.signal(signal.SIGTERM,signalHandler)
    signal.signal(signal.SIGINT,signalHandler)

    start_button.configure(command=start_app)
    exit_button.configure(command=exit_app)

if __name__ == "__main__":
    main()

tk.mainloop()
