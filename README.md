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