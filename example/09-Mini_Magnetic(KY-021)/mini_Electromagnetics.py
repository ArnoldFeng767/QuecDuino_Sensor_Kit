"""
@file      : mini_Electromagnetics.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based mini magnetic sensor project with output linkage control.
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime

class MiniMagneticController(object):
    """Mini magnetic sensor module control class."""

    def __init__(
        self,
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    ):
        # Typical scenario: After the door magnet is triggered, it increases the output, driving the warning light, buzzer or relay.
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PU)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.output_active_level = output_active_level
        self.output_inactive_level = 0 if output_active_level else 1
        self.last_state = self.sensor.read()

    # Read magnetic sensor
    def read_sensor(self):
        return self.sensor.read()
    

    def is_triggered(self):
        return self.read_sensor() == self.trigger_level

    # Output linkage control
    def set_output(self, active):
        level = self.output_active_level if active else self.output_inactive_level
        self.output.write(level)

    # Update output linkage based on sensor state, and return whether the state has changed and whether it is currently triggered.
    def update(self):
        state = self.read_sensor()
        triggered = state == self.trigger_level
        self.set_output(triggered)

        if triggered:
            print("Magnetic field change detected")
        else:
            print("No magnetic field change detected")

        changed = state != self.last_state
        self.last_state = state
        return changed, triggered

    def monitor(self):
        # Practical Applications: Periodic polling and output linkage, commonly used for access control status indication and intrusion detection.
        while True:
            changed, triggered = self.update()
            if changed:
                if triggered:
                    print("[MiniMagnetic] Event: trigger edge")
                else:
                    print("[MiniMagnetic] Event: release edge")
            utime.sleep(1)


def main():
    controller = MiniMagneticController(
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    )
    controller.monitor()
        

if __name__ == '__main__':
    main()