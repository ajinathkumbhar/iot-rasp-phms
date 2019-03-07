import os
from app.other import utils
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module
from gpiozero import Buzzer
from app.sensors.accevents import AccEvents
import event as evt
from app.reports.reportmail import Pimail

# LED_PULSE=31
# LED_TEMP=33
# LED_ACC_EVENT=37
# LED_ALERT=35

# Fllowing are GPIO number (not a pin number)
LED_PULSE=26
LED_TEMP=19
LED_ACC_EVENT=13
LED_ALERT=6
BUZZER_ALERT=21

TAG = os.path.basename(__file__)
mAccEvent = AccEvents()
mEmail = Pimail()

class Alert(object):
    def __init__(self):
        self.name = "Alert"
        self.pulse_limit = 80
        self.temp_limit = 40
        self.humidity_limit = 100
        self.ges_event_finger_limit = 3
        self.buzzer = Buzzer(BUZZER_ALERT)
        self.__is_high_alert = False
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
        GPIO.setup(LED_PULSE, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(LED_TEMP, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(LED_ACC_EVENT, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(LED_ALERT, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)

    def check_and_trigger_alert(self,sens_values):
        self.__pulse(sens_values.hbeat)
        self.__temp(sens_values.temp)
        self.__acc_event(sens_values.acc_event)
        self.__report_on_high_alert(sens_values)

    def __report_on_high_alert(self,sens_values):
        if not self.__is_high_alert:
            return
        mEmail.send(sens_values)
        self.__is_high_alert = False

    def __pulse(self,rate):
        if rate is None:
            val = 0
        utils.PLOGD(TAG,"pulse rate : " + str(rate))
        if int(rate) < self.pulse_limit:
            return
        # self.__is_high_alert = True
        self.__trigger_led(LED_PULSE,0.1)
        self.__trigger_buzzer()
        utils.PLOGD(TAG,"High pulse rate : " + str(rate))

    def __temp(self,val):
        if val is None:
            val = 0
        utils.PLOGD(TAG,"body temperature: " + str(val))
        if int(val) < self.temp_limit:
            return
        self.__is_high_alert = True
        self.__trigger_led(LED_TEMP,0.1)
        self.__trigger_buzzer()
        utils.PLOGD(TAG,"High body temperature: " + str(val))

    def __acc_event(self,event):
        if event[1] == evt.GES_EVENT_NONE:
            return
        utils.PLOGD(TAG, "Acc event : " + mAccEvent.get_event_str(event[1]))
        self.__trigger_led(LED_ACC_EVENT,0.1)

    def __trigger_led(self,LED_PIN,blink_delay=0):
        GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on
        sleep(blink_delay)  # Sleep for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn off
        sleep(blink_delay)  # Sleep for 1 second

    def __trigger_buzzer(self,timeout=0.3,beep=False):
        self.buzzer.off()
        self.buzzer.on()
        sleep(timeout)
        self.buzzer.off()
