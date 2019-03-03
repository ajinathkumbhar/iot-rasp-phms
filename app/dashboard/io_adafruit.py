# Example of using the MQTT client class to subscribe to and publish feed values.
# Import standard python modules.
import random
import sys
import time
from app.other import utils
import os
import datetime

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient
from app.reports.reportmail import Pimail
import Queue

TAG = os.path.basename(__file__)
mEmail = Pimail()
qSens = Queue.Queue(maxsize=1)

#----------------------------------------
feedDeviceID    = 'phmsdeviceid'
feedTemp        = 'phmstempstatus'
feedHumi        = 'phmshumistatus'
feedPulse       = 'phmspulsestatus'
feedLastOnline  = 'phmsstatus'
feedAccEventName = 'phmseventname'
feedAccEventTime = 'phmseventtime'
feedreport = 'phmsreport'


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'ce57f54de4464c2e8b2d2cccb2968072'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'ajinathkumbhar'
isClientConnected = False

mLast_sens_data = None


# Define callback functions which will be called when certain events happen.
def connected(client):
    utils.PLOGD(TAG,'Connected to Adafruit IO!  Listening for DemoFeed changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(feedreport)

def disconnected(client):
    # Disconnected function will be called when the mClient disconnects.
    utils.PLOGD(TAG,'Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    utils.PLOGD(TAG,'Feed {0} received new value: {1}'.format(feed_id, payload))
    if not qSens.empty() and int(payload):
        utils.PLOGD(TAG,'------ send report ---------------')
        sens = qSens.get()
        mEmail.send(sens)

class ioAdafruitDash():
    def __init__(self):
        self.mClient = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

    def setupClient(self):
        # Setup the callback functions defined above.
        self.mClient.on_connect    = connected
        self.mClient.on_disconnect = disconnected
        self.mClient.on_message    = message


        # Connect to the Adafruit IO server.
        self.mClient.connect()
        # The first option is to run a thread in the background so you can continue
        # doing things in your program.
        self.mClient.loop_background()

        print 'Connecting.',
        while not self.mClient.is_connected():
            print '.',
            time.sleep(.5)
   
    def update(self,sd):
        if not self.mClient.is_connected():
            utils.PLOGE(TAG,'Client not connected ... Check setupClient')
            return
        utils.PLOGD(TAG,"Update dashboard for : " + sd.device_id)
        self.mClient.publish(feedDeviceID, str(sd.device_id))
        self.mClient.publish(feedTemp, sd.temp)
        self.mClient.publish(feedHumi, sd.humi)
        self.mClient.publish(feedPulse, sd.hbeat)
        self.mClient.publish(feedAccEventTime, sd.acc_event[0])
        self.mClient.publish(feedAccEventName, sd.acc_event[1])
        self.mClient.publish(feedLastOnline, datetime.datetime.now().strftime("%Y-%B-%d %H:%M:%S"))

        if not qSens.empty():
            sens = qSens.get()
            utils.PLOGD(TAG,str(sens.temp))

        if not qSens.full():
            qSens.put(sd)

        
