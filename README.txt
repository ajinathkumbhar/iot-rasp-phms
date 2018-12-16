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
