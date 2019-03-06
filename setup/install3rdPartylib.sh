#!/bin/bash

echo "-----------------------------------------"
echo " install Adafruit_Python_ADS1x15"
echo "-----------------------------------------"

cd ../lib/Adafruit_Python_ADS1x15
sudo python setup.py install
cd ../

echo "-----------------------------------------"
echo " install mpu6050"
echo "-----------------------------------------"
cd ../lib/mpu6050
sudo python setup.py install
cd ../

echo "-----------------------------------------"
echo " install Adafruit_Python_SSD1306"
echo "-----------------------------------------"
cd ../lib/Adafruit_Python_SSD1306
sudo python setup.py install
cd ../

echo "-----------------------------------------"
echo " install Adafruit_Python_DHT"
echo "-----------------------------------------"
cd ../lib/Adafruit_Python_DHT
sudo python setup.py install
cd ../

