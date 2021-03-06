#!/bin/bash
sudo apt-get update &&
sudo apt-get install vim openssh-server openssh-client &&
sudo apt-get install python-pip
sudo apt-get install mosquitto
sudo apt-get install python-rpi.gpio
sudo apt-get install python-prctl
sudo pip install paho-mqtt
sudo pip install adafruit-io
sudo pip install enum 
sudo systemctl enable ssh 
sudo systemctl start ssh
sudo apt-get install -y python-imaging python-smbus i2c-tools
bash install3rdPartylib.sh
git clone https://github.com/Elecrow-keen/Elecrow-LCD35.git
cd Elecrow-LCD35
sudo ./Elecrow-LCD35
cd ../

#sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1
#sudo sysctl -w net.ipv6.conf.default.disable_ipv6=1
#chmod +x SetStaticIP.sh
#sudo ./SetStaticIP.sh


