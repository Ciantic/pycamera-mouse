#!/usr/bin/python3

from __future__ import absolute_import, print_function
import os
import sys
import dbus
import dbus.service
import dbus.mainloop.glib
import socket
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import logging

logging.basicConfig(level=logging.DEBUG)


class BtPiKeyboardMouseDevice:
    # change these constants
    MY_ADDRESS = "B8:27:EB:C5:B3:27"
    MY_DEV_NAME = "Raspberry Pi Keyboard and Mouse"

    # define some constants
    P_CTRL = 17  # Service port - must match port configured in SDP record
    P_INTR = 19  # Interrupt port - must match port configured in SDP record
    # dbus path of the bluez profile we will create
    # file path of the sdp record to load
    CURRENT_PATH = os.path.abspath(os.path.dirname(__file__))
    SDP_RECORD_PATH = CURRENT_PATH + "/sdp_record.xml"
    UUID = "00001124-0000-1000-8000-00805f9b34fb"

    def __init__(self):
        print("2. Setting up BT device")
        self.init_bt_device()
        self.init_bluez_profile()

    def init_bt_device(self):
        # https://linux.die.net/man/8/hciconfig

        print("3. Configuring Device name " + BtPiKeyboardMouseDevice.MY_DEV_NAME)
        os.system("hciconfig hci0 up")
        os.system(f"hciconfig hci0 name '{BtPiKeyboardMouseDevice.MY_DEV_NAME}'")
        os.system("hciconfig hci0 piscan") # Enable page and inquiry scan.

    def init_bluez_profile(self):
        print("4. Configuring Bluez Profile")

        # https://github.com/bluez/bluez/blob/master/doc/org.bluez.ProfileManager.rst
        #
        # setup profile options
        service_record = self.read_sdp_service_record()
        opts = {"AutoConnect": True, "ServiceRecord": service_record}
        bus = dbus.SystemBus()
        manager = dbus.Interface(
            bus.get_object("org.bluez", "/org/bluez"), "org.bluez.ProfileManager1"
        )
        manager.RegisterProfile("/org/bluez/hci0", BtPiKeyboardMouseDevice.UUID, opts)
        print("6. Profile registered ")

        # https://www.bluetooth.com/wp-content/uploads/Files/Specification/Assigned_Numbers.html#bookmark17
        #
        # Major service class: bits 13-23
        # Major device class:  bits 8-12
        # Minor device class:  bits 2-7
        #
        # Mouse + Keyboard:
        # Major service class: zeros
        # Major device class: 10th bit 1, 8th bit 1 = Peripheral (mouse, joystick, keyboard, ...)
        # Minor device class: 7th bit 1, 6th bit 1 = Combo Keyboard/Pointing Device
        #
        #        43219 9876 5432 1098 7654 3210
        #       0b0000_0000_0000_0101_1100_0000 = 0x5C0
        #
        # Minor device class is also used in SDP record HIDDeviceSubclass field
        os.system("hciconfig hci0 class 0x0005C0")

        # Turn on
        os.system("btmgmt discov on")
        os.system("btmgmt connectable on")
        os.system("btmgmt pairable on")
        os.system("btmgmt power on")

    def read_sdp_service_record(self):
        print("5. Reading service record")
        try:
            fh = open(BtPiKeyboardMouseDevice.SDP_RECORD_PATH, "r")
        except:
            sys.exit("Could not open the sdp record. Exiting...")
        return fh.read()

    def listen(self):
        print("\033[0;33m7. Waiting for connections\033[0m")
        self.scontrol = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP
        )
        self.sinterrupt = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP
        )
        self.scontrol.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sinterrupt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind these sockets to a port - port zero to select next available
        self.scontrol.bind((socket.BDADDR_ANY, self.P_CTRL))
        self.sinterrupt.bind((socket.BDADDR_ANY, self.P_INTR))

        # Start listening on the server sockets
        self.scontrol.listen(5)
        self.sinterrupt.listen(5)

        self.ccontrol, cinfo = self.scontrol.accept()
        print(
            "\033[0;32mGot a connection on the control channel from %s \033[0m"
            % cinfo[0]
        )

        self.cinterrupt, cinfo = self.sinterrupt.accept()
        print(
            "\033[0;32mGot a connection on the interrupt channel from %s \033[0m"
            % cinfo[0]
        )

    def send_string(self, message):
        try:
            self.cinterrupt.send(bytes(message))
        except OSError as err:
            logging.error(err)


# https://dbus.freedesktop.org/doc/dbus-python/dbus.service.html
#
# Custom DBUS service for this application
class BtPiKeyboardMouseService(dbus.service.Object):

    def __init__(self):
        print("1. Setting up service")
        bus_name = dbus.service.BusName("org.example.pikmservice", bus=dbus.SystemBus())
        dbus.service.Object.__init__(self, bus_name, "/org/example/pikmservice")
        self.device = BtPiKeyboardMouseDevice()
        self.device.listen()

    @dbus.service.method("org.example.pikmservice", in_signature="yay")
    def send_keys(self, modifier_byte, keys):
        # print("Get send_keys request through dbus")
        # print("key msg: ", keys)
        state = [0xA1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        state[2] = int(modifier_byte)
        count = 4
        for key_code in keys:
            if count < 10:
                state[count] = int(key_code)
            count += 1
        # print("keyboard state: ", state)
        self.device.send_string(state)

    @dbus.service.method("org.example.pikmservice", in_signature="yay")
    def send_mouse(self, modifier_byte, keys):
        # print("Get send_mouse request through dbus")
        # print("mouse msg: ", keys)
        state = [0xA1, 2, 0, 0, 0, 0]
        count = 2
        for key_code in keys:
            if count < 6:
                state[count] = int(key_code)
            count += 1
        # print("mouse state: ", state)
        self.device.send_string(state)


# main routine
if __name__ == "__main__":
    # we an only run as root
    try:
        if not os.geteuid() == 0:
            sys.exit("Only root can run this script")

        DBusGMainLoop(set_as_default=True)
        myservice = BtPiKeyboardMouseService()
        loop = GLib.MainLoop()
        loop.run()
    except KeyboardInterrupt:
        sys.exit()
