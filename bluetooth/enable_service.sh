#!/bin/bash

# Install the dbus service access control file
cp org.example.pikmservice.conf /etc/dbus-1/system.d/

# Ensure bluetooth service is not using the input plugin
sudo sed -i '/^ExecStart=/ {/--noplugin=input/! s/$/ --noplugin=input/}' /etc/systemd/system/bluetooth.target.wants/bluetooth.service

systemctl enable ./pikmbluetoothagent.service
systemctl enable ./pikmbluetooth.service
systemctl start pikmbluetooth.service
systemctl start pikmbluetoothagent.service