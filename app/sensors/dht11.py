import os
import Adafruit_DHT
from other import utils

TAG = os.path.basename(__file__)
sensor= Adafruit_DHT.DHT11
pin = 4

class THSensor:
    def __init__(self):
        self.name = "DHT11"

    def getSensorName(self):
        return self.name
    
    def getCurrTemp(self):
        print 'impl  getCurrTemp()'
        
    def getCurrHumidity(self):
        print 'Impl getCurrHumidity()'
    
    def getTHdata(self):
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        if humidity is None or temperature is None:
           utils.PLOGE(TAG,"Failed to get reading. Try again!")
        return humidity, temperature
        
        
