# Python Camera Mouse

Fork of https://github.com/stedwick/PhilNav-Python-RaspberryPi

This sends the cursor via a USB HID device, so it can be used without
networking. It should in theory work with iPads and other devices that support
USB mice.

## Installation

1. Install the dependencies:

OpenCV:

```
sudo apt install python3-opencv
```

Zero-HID (USB Gadget mode): https://github.com/thewh1teagle/zero-hid

## Hardware

Tested on Raspberry Pi 4 with the official camera module 3.

Plug *only* the USB-C cord from PC to Raspberry Pi. Data and power are going in
this one and same cable. USB mode does not work from Raspberry PI's A-type USB
ports, only via the USB-C power port.