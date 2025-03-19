#!/bin/bash

# Install the service
cp org.example.pikmservice.conf /etc/dbus-1/system.d/

if [ ! -L /etc/systemd/system/pikmbluetooth.service ]; then
    ln -s /home/pi/service/bluetooth/pikmbluetooth.service /etc/systemd/system/pikmbluetooth.service
fi
systemctl enable pikmbluetooth.service
systemctl start pikmbluetooth.service
# sudo btmgmt power off
btmgmt discov on
btmgmt connectable on
btmgmt pairable on
btmgmt power on

# = NoInputNoOutput, pairs automatically without user interaction
btmgmt io-cap 3 