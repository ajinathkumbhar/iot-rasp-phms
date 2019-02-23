# Example of using the MQTT client class to subscribe to and publish feed values.
# Import standard python modules.
import random
import sys
import time

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

#----------------------------------------

feedTemp        = 'phmstempstatus'
feedHumi        = 'phmshumistatus'
feedPulse       = 'phmspulsestatus'
feedAccGyro     = 'phmsaccgyrostatus'


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'ce57f54de4464c2e8b2d2cccb2968072'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'ajinathkumbhar'
isClientConnected = False


# Define callback functions which will be called when certain events happen.
def connected(client):
    print('Connected to Adafruit IO!  Listening for DemoFeed changes...')
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe('DemoFeed')

def disconnected(client):
    # Disconnected function will be called when the mClient disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)

def message(client, feed_id, payload):
    print('Feed {0} received new value: {1}'.format(feed_id, payload))


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
            print 'Client not connected ... Check setupClient'
            return
        # print '--------update ---------'
        self.mClient.publish(feedTemp, sd.temp)
        self.mClient.publish(feedHumi, sd.humi)
        self.mClient.publish(feedPulse, sd.hbeat)
        self.mClient.publish(feedAccGyro, sd.Az)
        
