import os
import Adafruit_DHT

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
           print('Failed to get reading. Try again!')
        return humidity, temperature
        
        
