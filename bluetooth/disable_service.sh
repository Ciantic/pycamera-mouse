#!/bin/bash

# Disable the service
rm /etc/dbus-1/system.d/org.example.pikmservice.conf
systemctl stop pikmbluetoothagent.service
systemctl stop pikmbluetooth.service
systemctl disable pikmbluetoothagent.service
systemctl disable pikmbluetooth.service
