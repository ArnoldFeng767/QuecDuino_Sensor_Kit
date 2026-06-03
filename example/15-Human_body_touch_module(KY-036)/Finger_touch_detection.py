"""
@file      : Finger_touch_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based finger touch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class TouchSensor:
    """Human touch sensor encapsulation class."""
    
    def __init__(self, pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD):
        self.gpio = Pin(pin, Pin.IN, pull)
        self.trigger_level = trigger_level

    def read_state(self):
        return self.gpio.read()

    def is_touched(self):
        return self.read_state() == self.trigger_level

    def monitor(self, interval_sec=1):
        while True:
            if self.is_touched():
                print("Touch detected")
            else:
                print("No touch detected")
            utime.sleep(interval_sec)

def main():
    touch_sensor = TouchSensor(pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD)
    touch_sensor.monitor(interval_sec=1)

if __name__ == '__main__':
    main()