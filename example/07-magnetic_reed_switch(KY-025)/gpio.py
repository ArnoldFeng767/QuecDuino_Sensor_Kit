"""
@file      : gpio.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based magnetic reed switch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class ReedSwitch(object):
    """Reed switch sensor encapsulation class."""

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        # Common wiring is pull-up input, output low when triggered.
        self.gpio = Pin(pin, Pin.IN, pull)
        self.trigger_level = trigger_level
        self.last_state = self.gpio.read()

    def read_state(self):
        return self.gpio.read()

    def is_triggered(self):
        return self.read_state() == self.trigger_level

    def check_state_change(self):
        current = self.read_state()
        changed = current != self.last_state
        self.last_state = current
        return changed, current

    def monitor(self, interval_sec=1):
        # Practical Applications: Door magnetic anti-theft, liquid level float switch, equipment in-place detection.
        # Trigger indicates a change in the magnetic field state (such as when a door is opened or closed).
        while True:
            changed, state = self.check_state_change()

            if changed:
                if state == self.trigger_level:
                    print("[ReedSwitch] Triggered: magnetic field change detected")
                else:
                    print("[ReedSwitch] Released: magnetic field back to normal")
            else:
                print("[ReedSwitch] Stable: no state change")

            utime.sleep(interval_sec)


def main():
    sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    sensor.monitor(interval_sec=1)


if __name__ == "__main__":
    main()