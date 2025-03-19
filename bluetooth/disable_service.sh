#!/bin/bash

# Disable the service
rm /etc/dbus-1/system.d/org.example.pikmservice.conf
systemctl stop pikmbluetooth.service
systemctl disable pikmbluetooth.service