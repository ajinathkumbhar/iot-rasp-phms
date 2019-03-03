#!/usr/bin/env python

import Tkinter as tk
import time
import os
import threading
import signal
import sys
from Tkinter import *
import  random

win = tk.Tk()
win.title("Phms")
# win.overrideredirect(True)
win.geometry("480x320")
lThreadsID = []
stop_threads = False
win.grid_columnconfigure(1, weight=1)

#font conf
font_large = (None, 14)
font_medium = (None, 12)
font_small = (None, 10)

# frames
title_frame = tk.Frame()
bt_frame = tk.Frame()
temp_frame = tk.Frame()
pulse_frame = tk.Frame()
acc_event_frame = tk.Frame()


# Title label frame
title = Label(title_frame, text="                               PHMS based on IoT", font=font_large, height=2)
title.pack(side="left", expand=False)
title_frame.grid(row=1, sticky=tk.W)

# Start and stop button
start_button = tk.Button(bt_frame, text='Start', bg='bisque2', font=font_medium, height=2, width=21)
exit_button = tk.Button(bt_frame, text='Exit', bg='bisque2', font=font_medium, height=2, width=21)
start_button.pack(side="left",fill=None, expand=False)
exit_button.pack(side="left",fill=None, expand=False)
bt_frame.grid(row=2, sticky=tk.W)

# temp sensor frame
temp_text = "Body temp:"
temp_val_string= StringVar()
temp_val_string.set("0")

temp_title = Label(temp_frame, text=temp_text, font=font_medium, height=3, width=25)
temp_val = Label( temp_frame, textvariable=temp_val_string, font=font_medium, height=3, width=25)

temp_title.pack(side="left", fill=None,expand=False)
temp_val.pack(side="left", fill=None,expand=False)

temp_frame.grid(row=3, sticky=tk.W)

# pulse sensor frame
pulse_text = "Pulse rate(per min) : "
pulse_val_string= StringVar()
pulse_val_string.set("0")

pulse_title = Label(pulse_frame, text=pulse_text, font=font_medium, height=3, width=25)
pulse_val = Label( pulse_frame, textvariable=pulse_val_string, font=font_medium, height=3, width=25)

pulse_title.pack(side="left", fill=None,expand=False)
pulse_val.pack(side="left", fill=None,expand=False)

pulse_frame.grid(row=4, sticky=tk.W)

# Accelerometer frame
acc_event_text = "Response : "
acc_event_val_string= StringVar()
acc_event_val_string.set("0")

acc_event_title = Label(acc_event_frame, text=acc_event_text, font=font_medium, height=3, width=25)
acc_event_val = Label( acc_event_frame, textvariable=acc_event_val_string, font=font_medium, height=3, width=25)

acc_event_title.pack(side="left", fill=None,expand=False)
acc_event_val.pack(side="left", fill=None,expand=False)

acc_event_frame.grid(row=5, sticky=tk.W)


#                   480
#      +------------------------------+
#      |                              |
#      |                              |
#      |                              |
#      |                              |
# 320  |                              |
#      |                              |
#      |                              |
#      |                              |
#      |                              |
#      +------------------------------+



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
        temp_val_string.set(str(random.randint(1,101)))
        pulse_val_string.set(str(random.randint(1,101)))
        acc_event_val_string.set(str(random.randint(1,101)))
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
