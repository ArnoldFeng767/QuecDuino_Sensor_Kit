"""
@file      : Inclination_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based inclination switch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class InclinationSwitch:
    """Tilt switch sensor packaging class."""

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        self.gpio = Pin(pin, Pin.IN, pull)
        self.led = Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        return self.gpio.read()

    def is_tilted(self):
        return self.read_state() == self.trigger_level

    def monitor(self):
        while True:
            if self.is_tilted():
                self.led.write(1)
                print("Tilt detected")
            else:
                self.led.write(0)
                print("Level state")
            utime.sleep(1)

def main():
    tilt_switch = InclinationSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    tilt_switch.monitor()

if __name__ == '__main__':
    main()