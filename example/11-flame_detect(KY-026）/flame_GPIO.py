"""
@file      : flame.py
@author    : Aaron Chen
@brief     : Class-based flame sensor demo using GPIO.
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class FlameDigitalSensor:
    """数字火焰传感器封装类。"""

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.last_state = self.sensor.read()

    def read_state(self):
        return self.sensor.read()

    def is_flame_detected(self):
        return self.read_state() == self.trigger_level

    def set_output(self, active):
        self.output.write(1 if active else 0)

    def update(self):
        state = self.read_state()
        detected = state == self.trigger_level
        self.set_output(detected)

        if detected:
            print("Flames were detected.")

        changed = state != self.last_state
        self.last_state = state
        return changed, detected

    def monitor(self):
        while True:
            self.update()
            utime.sleep_ms(100)


def main():
    flame_sensor = FlameDigitalSensor(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    flame_sensor.monitor()


if __name__ == "__main__":
    main()
        