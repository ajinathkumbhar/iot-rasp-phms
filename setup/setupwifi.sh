cat << EOF > wpa_supplicant.conf

ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

network={
    ssid="TX2"
    psk="TX2@rr112"
    scan_ssid=1
}
EOF

sudo cp wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf
sudo wpa_cli -i wlan0 reconfigure
rm wpa_supplicant.conf
