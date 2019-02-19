import os
from other import utils

TAG = os.path.basename(__file__)
class Alert:
    def __init__(self):
        self.name = "Alert"
        self.pulse_limit = 80
        self.temp_limit = 70
        self.humidity_limit = 100
        self.ges_event_finger_limit = 3

    def pulse(self,rate):
        if rate < self.pulse_limit:
            return

        utils.PLOGD(TAG,"High pulse rate : " + str(rate))

    def temp(self,val):
        if val < self.temp_limit:
            return

        utils.PLOGD(TAG,"High body temperature: " + str(val))

    def humidity(self,val):
        if val < self.temp_limit:
            return

        utils.PLOGD(TAG, "High humidity : " + str(val))
