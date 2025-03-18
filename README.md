# Python Camera Mouse

Fork of https://github.com/stedwick/PhilNav-Python-RaspberryPi

This sends the cursor via a USB HID device, so it can be used without
networking. It should in theory work with iPads and other devices that support
USB mice.

## Installation

### 1. Install the dependencies:

OpenCV:

```
sudo apt install python3-opencv
```

Zero-HID (USB Gadget mode): https://github.com/thewh1teagle/zero-hid (no need for Python library, only the usb_gadget module):

```
git clone https://github.com/thewh1teagle/zero-hid
cd zero-hid/usb_gadget
sudo ./installer
# reboot...
```

### 2. Install and test this application

This is made to work with Raspbian default home directory `/home/pi/`, but you can change the path in the `enable_service.sh` script:

```
git clone https://github.com/Ciantic/pycamera-mouse /home/pi/service/
cd /home/pi/service/
```

Now to test, send the preview image over the network to a remote display:

```
DISPLAY=192.168.8.122:0 ./main.py --preview
```

For instance works with [vcxsrv in Windows](https://github.com/marchaesen/vcxsrv/)


### 3. Installing as an auto starting systemd service

```
sudo ./enable_service.sh
```


## Hardware

Tested on Raspberry Pi 4 with the official camera module 3.

Plug *only* the USB-C cord from PC to Raspberry Pi. Data and power are going in
this one and same cable. USB mode does not work from Raspberry PI's A-type USB
ports, only via the USB-C power port.