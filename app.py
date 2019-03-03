#!/usr/bin/env python

import Tkinter as tk
import time
import os
import threading
import signal
import sys
from phms import PhmsCore
from phms import qSensor_data
from Tkinter import *
import app.other.utils as utils
from app.sensors.accevents import AccEvents
from app.reports.reportmail import Pimail
import Queue

TAG = os.path.basename(__file__)

# objects
mDevice_id = utils.get_device_id()
mPhms_core = PhmsCore(mDevice_id)
mAcc_event = AccEvents()
mEmail = Pimail()
qLast_sensor_data = Queue.Queue(maxsize=1)

# thread list to send kill signal
lThreadsID = []

# Window config
win = tk.Tk()
win.title("Phms")
win.overrideredirect(True)
win.geometry("480x320")
win.grid_columnconfigure(1, weight=1)

#font conf
font_large = (None, 14)
font_medium = (None, 12)
font_small = (None, 10)

# frames
title_frame = tk.Frame()
bt_frame = tk.Frame()
id_frame = tk.Frame()
temp_frame = tk.Frame()
pulse_frame = tk.Frame()
acc_event_frame = tk.Frame()
report_frame = tk.Frame()

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

# Device ID frame
id_text = "Device ID:"
id_val_string= StringVar()
id_val_string.set(mDevice_id)

id_title = Label(id_frame, text=id_text, font=font_medium, height=2, width=15)
id_val = Label( id_frame, textvariable=id_val_string, font=font_medium, height=2, width=35)

id_title.pack(side="left", fill=None,expand=False)
id_val.pack(side="left", fill=None,expand=False)

id_frame.grid(row=3, sticky=tk.W)

# temp sensor frame
temp_text = "Body temp:"
temp_val_string= StringVar()
temp_val_string.set("0")

temp_title = Label(temp_frame, text=temp_text, font=font_medium, height=2, width=15)
temp_val = Label( temp_frame, textvariable=temp_val_string, font=font_medium, height=2, width=35)

temp_title.pack(side="left", fill=None,expand=False)
temp_val.pack(side="left", fill=None,expand=False)

temp_frame.grid(row=4, sticky=tk.W)



# pulse sensor frame
pulse_text = "Pulse rate : "
pulse_val_string= StringVar()
pulse_val_string.set("0")

pulse_title = Label(pulse_frame, text=pulse_text, font=font_medium, height=2, width=15)
pulse_val = Label( pulse_frame, textvariable=pulse_val_string, font=font_medium, height=2, width=35)

pulse_title.pack(side="left", fill=None,expand=False)
pulse_val.pack(side="left", fill=None,expand=False)

pulse_frame.grid(row=5, sticky=tk.W)

# Accelerometer frame
acc_event_text = "Last response : "
acc_event_val_string= StringVar()
acc_event_val_string.set("0")

acc_event_title = Label(acc_event_frame, text=acc_event_text, font=font_medium, height=2, width=15)
acc_event_val = Label( acc_event_frame, textvariable=acc_event_val_string, font=font_medium, height=2, width=35)

acc_event_title.pack(side="left", fill=None,expand=False)
acc_event_val.pack(side="left", fill=None,expand=False)

acc_event_frame.grid(row=6, sticky=tk.W)

# report button
report_button = tk.Button(report_frame, text='Send report', bg='bisque2', font=font_medium, height=2, width=21)
report_button.pack(side="left",fill=None, expand=False)
report_frame.grid(row=7, sticky=tk.W)

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
    mPhms_core.stop_app()
    sys.exit(0)

def run_app():
    mPhms_core.start_app()


def send_email():
    mEmail.send(qLast_sensor_data.get())
    utils.PLOGD(TAG, "@@@ Report sent ")

def send_report():
    if qLast_sensor_data.empty():
        utils.PLOGD(TAG, "@@@ Report data available ")
        return

    email_thread = threading.Thread(target=send_email)
    lThreadsID.append(email_thread)
    email_thread.start()

def update_ui():
    while True:
        if qSensor_data.empty():
            time.sleep(0.1)
            continue
        report_button.configure(state="normal")
        sens_data = qSensor_data.get()

        if qLast_sensor_data.empty():
            qLast_sensor_data.put(sens_data)
        else:
            qLast_sensor_data.get(sens_data)
            qLast_sensor_data.put(sens_data)

        utils.PLOGD(TAG,"-------- ui_thread " + str(sens_data.temp))
        utils.PLOGD(TAG,"-------- ui_thread " + str(sens_data.humi))
        utils.PLOGD(TAG,"-------- ui_thread " + str(sens_data.hbeat))
        utils.PLOGD(TAG,"-------- ui_thread " + str(mAcc_event.get_event_str(sens_data.acc_event[1])))
        temp_val_string.set(str(sens_data.temp))
        pulse_val_string.set(str(sens_data.hbeat))

        event_str = " - "
        if sens_data.acc_event[1] ==  0x07:
            event_str =  "HAND FLIP" + event_str + sens_data.acc_event[0]
        elif sens_data.acc_event[1] ==  0x01:
            event_str =  "FINGER UP" + event_str  + sens_data.acc_event[0]
        else:
            event_str = "None"
        acc_event_val_string.set(event_str)

def start_app():
    app_thread = threading.Thread(target=run_app)
    ui_thread = threading.Thread(target=update_ui)

    lThreadsID.append(app_thread)
    lThreadsID.append(ui_thread)
    app_thread.start()
    ui_thread.start()
    start_button.configure(state="disabled")


def exit_app():
    os.kill(os.getpid(), signal.SIGTERM)

def main():
    signal.signal(signal.SIGTERM,signalHandler)
    signal.signal(signal.SIGINT,signalHandler)

    start_button.configure(command=start_app)
    exit_button.configure(command=exit_app)
    report_button.configure(command=send_report)
    report_button.configure(state="disabled")


if __name__ == "__main__":
    main()

tk.mainloop()
