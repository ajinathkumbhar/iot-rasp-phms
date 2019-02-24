import os
from other import utils
import RPi.GPIO as GPIO  # Import Raspberry Pi GPIO library
from time import sleep  # Import the sleep function from the time module

# LED_PULSE=31
# LED_TEMP=33
# LED_ACC_EVENT=37
# LED_ALERT=35

LED_PULSE=26
LED_TEMP=19
LED_ACC_EVENT=13
LED_ALERT=6

TAG = os.path.basename(__file__)
class Alert:
    def __init__(self):
        self.name = "Alert"
        self.pulse_limit = 80
        self.temp_limit = 70
        self.humidity_limit = 100
        self.ges_event_finger_limit = 3
        GPIO.setwarnings(False)  # Ignore warning for now
        GPIO.setmode(GPIO.BCM)  # Use physical pin numbering
        GPIO.setup(LED_PULSE, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(LED_TEMP, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(LED_ACC_EVENT, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.setup(LED_ALERT, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)

    def check_and_trigger_alert(self,sens_values):
        self.__pulse(sens_values.hbeat)
        self.__temp(sens_values.temp)

    def __pulse(self,rate):
        utils.PLOGD(TAG,"pulse rate : " + str(rate))
        if int(rate) < self.pulse_limit:
            return
        self.__trigger_led(LED_PULSE,0.3)
        utils.PLOGD(TAG,"High pulse rate : " + str(rate))

    def __temp(self,val):
        utils.PLOGD(TAG,"body temperature: " + str(val))
        if int(val) < self.temp_limit:
            return
        self.__trigger_led(LED_TEMP,0.3)
        utils.PLOGD(TAG,"High body temperature: " + str(val))

    def __trigger_led(self,LED_PIN,blink_delay=0):
        GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)  # Set pin 8 to be an output pin and set initial value to low (off)
        GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on
        sleep(blink_delay)  # Sleep for 1 second
        GPIO.output(LED_PIN, GPIO.LOW)  # Turn off
        sleep(blink_delay)  # Sleep for 1 second

