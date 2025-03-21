#!/usr/bin/python3
import sys  # used to exit the script
import dbus
import dbus.service
import dbus.mainloop.glib
import time


keytable = {
    "KEY_RESERVED" : 0,
    "KEY_ESC" : 41,
    "KEY_1" : 30,
    "KEY_2" : 31,
    "KEY_3" : 32,
    "KEY_4" : 33,
    "KEY_5" : 34,
    "KEY_6" : 35,
    "KEY_7" : 36,
    "KEY_8" : 37,
    "KEY_9" : 38,
    "KEY_0" : 39,
    "KEY_MINUS" : 45,
    "KEY_EQUAL" : 46,
    "KEY_BACKSPACE" : 42,
    "KEY_TAB" : 43,
    "KEY_Q" : 20,
    "KEY_W" : 26,
    "KEY_E" : 8,
    "KEY_R" : 21,
    "KEY_T" : 23,
    "KEY_Y" : 28,
    "KEY_U" : 24,
    "KEY_I" : 12,
    "KEY_O" : 18,
    "KEY_P" : 19,
    "KEY_LEFTBRACE" : 47,
    "KEY_RIGHTBRACE" : 48,
    "KEY_ENTER" : 40,
    "KEY_LEFTCTRL" : 224,
    "KEY_A" : 4,
    "KEY_S" : 22,
    "KEY_D" : 7,
    "KEY_F" : 9,
    "KEY_G" : 10,
    "KEY_H" : 11,
    "KEY_J" : 13,
    "KEY_K" : 14,
    "KEY_L" : 15,
    "KEY_SEMICOLON" : 51,
    "KEY_APOSTROPHE" : 52,
    "KEY_GRAVE" : 53,
    "KEY_LEFTSHIFT" : 225,
    "KEY_BACKSLASH" : 50,
    "KEY_Z" : 29,
    "KEY_X" : 27,
    "KEY_C" : 6,
    "KEY_V" : 25,
    "KEY_B" : 5,
    "KEY_N" : 17,
    "KEY_M" : 16,
    "KEY_COMMA" : 54,
    "KEY_DOT" : 55,
    "KEY_SLASH" : 56,
    "KEY_RIGHTSHIFT" : 229,
    "KEY_KPASTERISK" : 85,
    "KEY_LEFTALT" : 226,
    "KEY_SPACE" : 44,
    "KEY_CAPSLOCK" : 57,
    "KEY_F1" : 58,
    "KEY_F2" : 59,
    "KEY_F3" : 60,
    "KEY_F4" : 61,
    "KEY_F5" : 62,
    "KEY_F6" : 63,
    "KEY_F7" : 64,
    "KEY_F8" : 65,
    "KEY_F9" : 66,
    "KEY_F10" : 67,
    "KEY_NUMLOCK" : 83,
    "KEY_SCROLLLOCK" : 71,
    "KEY_KP7" : 95,
    "KEY_KP8" : 96,
    "KEY_KP9" : 97,
    "KEY_KPMINUS" : 86,
    "KEY_KP4" : 92,
    "KEY_KP5" : 93,
    "KEY_KP6" : 94,
    "KEY_KPPLUS" : 87,
    "KEY_KP1" : 89,
    "KEY_KP2" : 90,
    "KEY_KP3" : 91,
    "KEY_KP0" : 98,
    "KEY_KPDOT" : 99,
    "KEY_ZENKAKUHANKAKU" : 148,
    "KEY_102ND" : 100,
    "KEY_F11" : 68,
    "KEY_F12" : 69,
    "KEY_RO" : 135,
    "KEY_KATAKANA" : 146,
    "KEY_HIRAGANA" : 147,
    "KEY_HENKAN" : 138,
    "KEY_KATAKANAHIRAGANA" : 136,
    "KEY_MUHENKAN" : 139,
    "KEY_KPJPCOMMA" : 140,
    "KEY_KPENTER" : 88,
    "KEY_RIGHTCTRL" : 228,
    "KEY_KPSLASH" : 84,
    "KEY_SYSRQ" : 70,
    "KEY_RIGHTALT" : 230,
    "KEY_HOME" : 74,
    "KEY_UP" : 82,
    "KEY_PAGEUP" : 75,
    "KEY_LEFT" : 80,
    "KEY_RIGHT" : 79,
    "KEY_END" : 77,
    "KEY_DOWN" : 81,
    "KEY_PAGEDOWN" : 78,
    "KEY_INSERT" : 73,
    "KEY_DELETE" : 76,
    "KEY_MUTE" : 239,
    "KEY_VOLUMEDOWN" : 238,
    "KEY_VOLUMEUP" : 237,
    "KEY_POWER" : 102,
    "KEY_KPEQUAL" : 103,
    "KEY_PAUSE" : 72,
    "KEY_KPCOMMA" : 133,
    "KEY_HANGEUL" : 144,
    "KEY_HANJA" : 145,
    "KEY_YEN" : 137,
    "KEY_LEFTMETA" : 227,
    "KEY_RIGHTMETA" : 231,
    "KEY_COMPOSE" : 101,
    "KEY_STOP" : 243,
    "KEY_AGAIN" : 121,
    "KEY_PROPS" : 118,
    "KEY_UNDO" : 122,
    "KEY_FRONT" : 119,
    "KEY_COPY" : 124,
    "KEY_OPEN" : 116,
    "KEY_PASTE" : 125,
    "KEY_FIND" : 244,
    "KEY_CUT" : 123,
    "KEY_HELP" : 117,
    "KEY_CALC" : 251,
    "KEY_SLEEP" : 248,
    "KEY_WWW" : 240,
    "KEY_COFFEE" : 249,
    "KEY_BACK" : 241,
    "KEY_FORWARD" : 242,
    "KEY_EJECTCD" : 236,
    "KEY_NEXTSONG" : 235,
    "KEY_PLAYPAUSE" : 232,
    "KEY_PREVIOUSSONG" : 234,
    "KEY_STOPCD" : 233,
    "KEY_REFRESH" : 250,
    "KEY_EDIT" : 247,
    "KEY_SCROLLUP" : 245,
    "KEY_SCROLLDOWN" : 246,
    "KEY_F13" : 104,
    "KEY_F14" : 105,
    "KEY_F15" : 106,
    "KEY_F16" : 107,
    "KEY_F17" : 108,
    "KEY_F18" : 109,
    "KEY_F19" : 110,
    "KEY_F20" : 111,
    "KEY_F21" : 112,
    "KEY_F22" : 113,
    "KEY_F23" : 114,
    "KEY_F24" : 115
}

# Map modifier keys to array element in the bit array
modkeys = {
    "KEY_RIGHTMETA" : 0,
    "KEY_RIGHTALT" : 1,
    "KEY_RIGHTSHIFT" : 2,
    "KEY_RIGHTCTRL" : 3,
    "KEY_LEFTMETA" : 4,
    "KEY_LEFTALT": 5,
    "KEY_LEFTSHIFT": 6,
    "KEY_LEFTCTRL": 7
}

def convert(evdev_keycode):
    return keytable[evdev_keycode]

def modkey(evdev_keycode):
    if evdev_keycode in modkeys:
        return modkeys[evdev_keycode]
    else:
        return -1 # Return an invalid array element

class BtkStringClient():
    # constants
    KEY_DOWN_TIME = 0.01
    KEY_DELAY = 0.01

    def __init__(self):
        # the structure for a bt keyboard input report (size is 10 bytes)
        self.state = [
            0xA1,  # this is an input report
            0x01,  # Usage report = Keyboard
            # Bit array for Modifier keys
            [0,  # Right GUI - Windows Key
                 0,  # Right ALT
                 0,  # Right Shift
                 0,  # Right Control
                 0,  # Left GUI
                 0,  # Left ALT
                 0,  # Left Shift
                 0],  # Left Control
            0x00,  # Vendor reserved
            0x00,  # rest is space for 6 keys
            0x00,
            0x00,
            0x00,
            0x00,
            0x00]
        self.scancodes = {
            "-": "KEY_MINUS",
            "=": "KEY_EQUAL",
            ";": "KEY_SEMICOLON",
            "'": "KEY_APOSTROPHE",
            "`": "KEY_GRAVE",
            "\\": "KEY_BACKSLASH",
            ",": "KEY_COMMA",
            ".": "KEY_DOT",
            "/": "KEY_SLASH",
            "_": "key_minus",
            "+": "key_equal",
            ":": "key_semicolon",
            "\"": "key_apostrophe",
            "~": "key_grave",
            "|": "key_backslash",
            "<": "key_comma",
            ">": "key_dot",
            "?": "key_slash",
            " ": "KEY_SPACE",
        }

        # connect with the Bluetooth keyboard server
        print("setting up DBus Client")
        self.bus = dbus.SystemBus()
        self.btkservice = self.bus.get_object(
            'org.example.pikmservice', '/org/example/pikmservice')
        self.iface = dbus.Interface(self.btkservice, 'org.example.pikmservice')

    def send_key_state(self):
        """sends a single frame of the current key state to the emulator server"""
        bin_str = ""
        element = self.state[2]
        for bit in element:
            bin_str += str(bit)
        self.iface.send_keys(int(bin_str, 2), self.state[4:10])

    def send_key_down(self, scancode, modifiers):
        """sends a key down event to the server"""
        self.state[2] = modifiers
        self.state[4] = scancode
        self.send_key_state()

    def send_key_up(self):
        """sends a key up event to the server"""
        self.state[4] = 0
        self.send_key_state()

    def send_string(self, string_to_send):
        for c in string_to_send:
            cu = c.upper()
            modifiers = [ 0, 0, 0, 0, 0, 0, 0, 0 ]
            if cu in self.scancodes:
                scantablekey = self.scancodes[cu]
                if scantablekey.islower():
                    modifiers = [ 0, 0, 0, 0, 0, 0, 1, 0 ]
                    scantablekey = scantablekey.upper()
            else:
                if c.isupper():
                    modifiers = [ 0, 0, 0, 0, 0, 0, 1, 0 ]
                scantablekey = "KEY_" + cu

            scancode = keytable[scantablekey]
            self.send_key_down(scancode, modifiers)
            time.sleep(BtkStringClient.KEY_DOWN_TIME)
            self.send_key_up()
            time.sleep(BtkStringClient.KEY_DELAY)


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Usage: send_string <string to send>")
        exit()
    dc = BtkStringClient()
    string_to_send = sys.argv[1]
    print("Sending " + string_to_send + " after 3 seconds...")
    time.sleep(3)
    dc.send_string(string_to_send)
    print("Done.")