"""
@file      : key_ExtInt.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based key interrupt example for QuecPython
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

import utime
from machine import ExtInt, Pin


class KeyInterrupt(object):

    def __init__(self, pin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_PU, filter_time=50, user_callback=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        self.filter_time = filter_time
        self.user_callback = user_callback
        self.press_count = 0
        self._extint = ExtInt(self.pin, self.mode, self.pull, self._irq_handler, self.filter_time)

    def _irq_handler(self, args):
        self.press_count += 1
        print("[KeyInterrupt] key pressed, count = {}".format(self.press_count))
        if self.user_callback:
            self.user_callback(args, self.press_count)

    def enable(self):
        self._extint.enable()

    def disable(self):
        self._extint.disable()

    def reset_count(self):
        self.press_count = 0


def on_key_pressed(args, count):
    print("[UserCallback] args = {}, count = {}".format(args, count))


if __name__ == "__main__":
    # Modify according to the actual pins of your development board, for example, Pin.GPIO31
    key = KeyInterrupt(
        pin=Pin.GPIO31,
        mode=ExtInt.IRQ_FALLING,
        pull=Pin.PULL_PU,
        filter_time=50,
        user_callback=on_key_pressed,
    )
    key.enable()

    print("Key interrupt is enabled. Press the key to trigger interrupt.")
    while True:
        utime.sleep_ms(500)



