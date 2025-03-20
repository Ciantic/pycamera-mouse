import math
from dataclasses import dataclass
from collections import deque  # for storing x, y time series
from time import time
import dbus

# Original values by Phil
# speed = 25
# smooth = 3
# smooth_long = smooth * 3 + 1
# deadzone = 0.03
# scaling_y = 1.25
# scaling_x = 1

# invert_x = -1
# invert_y = -1

speed = 40
smooth = 3
smooth_long = smooth * 3 + 1
deadzone = 0.03
scaling_y = 1.25
scaling_x = 1
invert_x = -1
invert_y = -1
use_bluetooth = False
use_usb = True
mouse_hid_device = None
bus = None
btiface = None
now = time()


def smoother(q):
    avg = sum(q) / len(q)
    return avg


def set_relative_mouse(x, y):
    global mouse_hid_device
    if mouse_hid_device is None:
        mouse_hid_device = open("/dev/hidg1", "wb")
    mouse_hid_device.seek(0)
    buttons = 0x0
    vertical_wheel_delta = 0
    horizontal_wheel_delta = 0
    if x >= 127 or x <= -127:
        print(f"x size problem {x}")
    if y >= 127 or y <= -127:
        print(f"y size problem {y}")

    buf = [
        buttons,
        int(x) & 0xFF,
        int(y) & 0xFF,
        vertical_wheel_delta & 0xFF,
        horizontal_wheel_delta & 0xFF,
    ]

    mouse_hid_device.write(bytes(buf))
    mouse_hid_device.flush()


def set_relative_mouse_bt(x, y):
    global bus, btiface
    state = [0, int(x) & 0xFF, int(y) & 0xFF, 0]
    if btiface is None:
        bus = dbus.SystemBus()
        btproxy = bus.get_object("org.example.pikmservice", "/org/example/pikmservice")
        btiface = dbus.Interface(btproxy, "org.example.pikmservice")
    btiface.send_mouse(0, bytes(state))


@dataclass
class datacache:
    time_start = now
    time_last_moved = now
    time_debug = now
    time_heartbeat = now
    debug_num = 0
    x_q = deque([], smooth)
    x_q_smooth = 0
    x_q_long = deque([], smooth_long)
    x_q_long_smooth = 0
    y_q = deque([], smooth)
    y_q_smooth = 0
    y_q_long = deque([], smooth_long)
    y_q_long_smooth = 0


phil2 = datacache()


def custom_sender_to_mouse(x_diff, y_diff, time_cam, ms_opencv):

    # store recent mouse movements
    phil2.x_q.append(x_diff)
    phil2.x_q_smooth = smoother(phil2.x_q)
    phil2.y_q.append(y_diff)
    phil2.y_q_smooth = smoother(phil2.y_q)
    phil2.x_q_long.append(x_diff)
    phil2.x_q_long_smooth = smoother(phil2.x_q_long)
    phil2.y_q_long.append(y_diff)
    phil2.y_q_long_smooth = smoother(phil2.y_q_long)

    # Perform more smoothing the *slower* the mouse is moving.
    # A slow-moving cursor means the user is trying to precisely
    # point at something.
    if x_diff**2 + y_diff**2 < 0.2:  # more smoothing
        x_smooth = phil2.x_q_long_smooth
        y_smooth = phil2.y_q_long_smooth
    elif x_diff**2 + y_diff**2 < 0.5:  # less smoothing
        x_smooth = phil2.x_q_smooth
        y_smooth = phil2.y_q_smooth
    else:  # moving fast, no smoothing
        x_smooth = x_diff
        y_smooth = y_diff

    # Prevent small jittering when holding mouse cursor still inside deadzone.
    accel_avg = math.sqrt(phil2.x_q_smooth**2 + phil2.y_q_smooth**2)
    if accel_avg > 0 and accel_avg < deadzone:
        return

    x_new_diff = x_smooth * speed * scaling_x * invert_x
    y_new_diff = y_smooth * speed * scaling_y * invert_y

    if use_usb:
        set_relative_mouse(x_new_diff, y_new_diff)

    if use_bluetooth:
        set_relative_mouse_bt(x_new_diff, y_new_diff)
    # zerohidmouse.move(x_new_diff, y_new_diff)
    # zerohidmouse.move(int(x_new_diff) % 128, int(y_new_diff) % 128)
    # print(f"Mouse movement: {set_diff_x}, {set_diff_y}")
