#!/usr/bin/env python3
# Agent that auto accepts the pairing request
#
# Must be run in background as root user

import dbus
import dbus.service
import dbus.mainloop.glib
from gi.repository import GLib

MY_AGENT_PATH = "/org/example/agent"
CAPABILITY = "KeyboardDisplay"

bus = None
mainloop = None


def set_trusted(device_path):
    proxy = bus.get_object("org.bluez", device_path)
    proxy.Set(
        "org.bluez.Device1",
        "Trusted",
        True,
        dbus_interface="org.freedesktop.DBus.Properties",
    )


class Rejected(dbus.DBusException):
    _dbus_error_name = "org.bluez.Error.Rejected"


# https://dbus.freedesktop.org/doc/dbus-python/dbus.service.html
# https://github.com/bluez/bluez/blob/master/doc/org.bluez.Agent.rst
class Agent(dbus.service.Object):
    @dbus.service.method("org.bluez.Agent1", in_signature="", out_signature="")
    def Release(self):
        mainloop.quit()

    @dbus.service.method("org.bluez.Agent1", in_signature="ou", out_signature="")
    def RequestConfirmation(self, device_path, passkey):
        # https://github.com/bluez/bluez/blob/master/doc/org.bluez.Device.rst
        print("Trust device (%s, %06d)" % (device_path, passkey))
        set_trusted(device_path)


if __name__ == "__main__":
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    agent = Agent(bus, MY_AGENT_PATH)
    mainloop = GLib.MainLoop()
    manager = dbus.Interface(
        bus.get_object("org.bluez", "/org/bluez"), "org.bluez.AgentManager1"
    )
    manager.RegisterAgent(MY_AGENT_PATH, CAPABILITY)
    manager.RequestDefaultAgent(MY_AGENT_PATH)
    print("Agent registered")
    mainloop.run()
