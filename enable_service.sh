#!/bin/bash

# Install the service

if [ ! -L /etc/systemd/system/mousesender.service ]; then
    ln -s /home/pi/service/mousesender.service /etc/systemd/system/mousesender.service
fi
systemctl enable mousesender.service
systemctl start mousesender.service