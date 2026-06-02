"""
@file      : mercury_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based mercury switch detection using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime

class MercurySwitch:
    """Mercury switch sensor encapsulation class."""

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU):
        self.sensor = Pin(sensor_pin, Pin.IN, pull)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        return self.sensor.read()

    def is_triggered(self):
        return self.read_state() == self.trigger_level

    def update(self):
        if self.is_triggered():
            self.output.write(1)
            print("Mercury detected inclination")
        else:
            self.output.write(0)
            print("Mercury did not detect inclination")

    def monitor(self):
        while True:
            self.update()
            utime.sleep(1)

def main():
    mercury = MercurySwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU)
    mercury.monitor()

if __name__ == '__main__':
    main()
