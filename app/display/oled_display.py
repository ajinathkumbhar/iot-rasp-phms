import os
import Adafruit_SSD1306
import time
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from sensors.sensor_utils import SensData
from other import utils

import subprocess

TAG = os.path.basename(__file__)
# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used

disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)
# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

ROW_MIDDLE = (128/2 - 1)
COL_MIDDLE = (64/2 - 1)


class OLEDDisplay:
    def __init__(self):
        self.name = 'SD1306'
        self.disp = None

    def setupDisplay(self):
        utils.PLOGD(TAG,"setupDisplay ---ok")

    def testDisplay(self):

        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d\' \' -f1"
        IP = subprocess.check_output(cmd, shell = True )
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )

        # Write two lines of text.

        draw.text((x, top),       "IP: " + str(IP),  font=font, fill=255)
        draw.text((x, top+8),     str(CPU), font=font, fill=255)
        draw.text((x, top+16),    str(MemUsage),  font=font, fill=255)
        draw.text((x, top+25),    str(Disk),  font=font, fill=255)

        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.1)

    def showWithDefaultTheme(self,sd):
        # print 'From display class'
        # print 'temperature : ' + str(sd.temp)
        # print 'humidity    : ' + str(sd.humi)
        # print 'Gx          : ' + str(sd.Gx)
        # print 'Gy          : ' + str(sd.Gy)
        # print 'Gz          : ' + str(sd.Gz)
        # print 'Ax          : ' + str(sd.Ax)
        # print 'Ay          : ' + str(sd.Ay)
        # print 'Az          : ' + str(sd.Az)
        # print 'Pulses      : ' + str(sd.hbeat)
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x, top),"Temp: " + str(sd.temp),  font=font, fill=255)
        draw.text((x + ROW_MIDDLE, top),"Humi: " + str(sd.humi),  font=font, fill=255)
        draw.text((x, top + 8), "Gx: " + str(sd.Gx),  font=font, fill=255)
        draw.text((x, top + 16),"Gy: " + str(sd.Gy),  font=font, fill=255)
        draw.text((x, top + 24),"Gz: " + str(sd.Gz),  font=font, fill=255)
        draw.text((x, top + 32),"Ax: " + str(sd.Ax),  font=font, fill=255)
        draw.text((x, top + 40),"Ay: " + str(sd.Ay),  font=font, fill=255)
        draw.text((x, top + 48),"Az: " + str(sd.Az),  font=font, fill=255)
        draw.text((x, top + 56),"HB: " + str(sd.hbeat),  font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(.1)

