1. Setup Adafruit SSD1306 display lib

git clone https://github.com/adafruit/Adafruit_Python_SSD1306.git
cd Adafruit_Python_SSD1306
python setup.py --install




                                                                                              +           +------------------+
             +-----------+                                        +--------------------+      |           |Desktop computer  |
             | OLED      |                                        | io.adafruit.com    |http  +----------->                  |
             | display   |                               +------> | dashboard          +------>           |                  |
             +-----^-----+                               | +------+                    |      |           +------------------+
                   |i2c                                  | |      +---------+----------+      |
                   |                                     | |                |                 |
          +--------+---------+                           | |                |                 |
          |Raspberry pi 3    |          MQTT             | |      +---------v----------+      |           +------------------+
          |Data acquisition  +---------------------------+ |      |  IFTTT cloud       |      |           | Laptop           |
          |& data proccessor <-----------------------------+      |                    |      |           |                  |
          +-------+----------+                                    |                    |      +----------->                  |
     +-----^      ^     ^--------+                                +---------+----------+      |           |                  |
     |SPI         |i2c           |i2c                                       |                 |           +------------------+
     |            |              |                                          |                 |
+----+--+     +---+----+    +----+---+                            +---------v----------+      |
| Temp  |     |Pulse   |    |Acc &   |                            | Gmail server       |      |           +------------------+
| Sensor|     |sensor  |    |Gyro    |                            |                    +------>           |  Smartphone      |
+-------+     +--------+    +--------+                            |                    |      |           |                  |
                                                                  +--------------------+      +----------->                  |
                                                                                                          |                  |
                                                                                                          +------------------+


####################################################333
https://io.adafruit.com

temperature - phms/temp/status      - value  - Guage meter
humidity    - phms/humi/status      - value  - Guage meter
pulse sensor - phms/pulse/status    - value  - Line chart with time
Acc &  Gyro  - phms/accGyro/status  - Angle Value/Alarm - Button

Other info.
-----------
Health email alert - phms/alert/email/critical - Text - Text
Fever email alert - phms/alert/email/feverCritical - Text - Text
Pulse Low email alert - phms/alert/email/pulseLow - Text - Text
Pulse High email alert - phms/alert/email/pulseHigh - Text - Text



