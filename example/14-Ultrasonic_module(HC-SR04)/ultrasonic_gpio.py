"""
@file      : ultrasonic_gpio.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based ultrasonic distance measurement using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class UltrasonicSensor(object):
    """Ultrasonic distance measurement module packaging class."""

    def __init__(self, trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5):
        self.trig = Pin(trig_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.echo = Pin(echo_pin, Pin.IN, Pin.PULL_DISABLE, 0)
        self.filter_size = filter_size
        self.dist_list = []

    # Send a high-level trigger signal for more than 10us
    def _trigger(self):
        self.trig.off()
        utime.sleep_us(2)
        self.trig.on()
        utime.sleep_us(10)
        self.trig.off()

    # Read the distance
    def read_distance(self):
        self._trigger()

        t_out = 0
        while self.echo.value() == 0 and t_out < 30000:
            t_out += 1
        if t_out >= 30000:
            return None

        start = utime.ticks_us()

        t_out = 0
        while self.echo.value() == 1 and t_out < 500000:
            t_out += 1
        if t_out >= 500000:
            return None

        end = utime.ticks_us()
        duration = end - start
        distance = duration / 58.0
        return round(distance, 2)

 
    # Read the filtered distance
    def read_filtered_distance(self):
        raw_dist = self.read_distance()
        if raw_dist is None or not 2 <= raw_dist <= 800:
            return None

        self.dist_list.append(raw_dist)
        if len(self.dist_list) > self.filter_size:
            self.dist_list.pop(0)
        return round(sum(self.dist_list) / len(self.dist_list), 2)

    # Monitor the distance
    def monitor(self, interval_ms=200):
        while True:
            avg_dist = self.read_filtered_distance()
            if avg_dist is not None:
                print("Current distance:", avg_dist, "cm")
            else:
                print("Out of range or signal error")
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    ultrasonic = UltrasonicSensor(trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5)
    ultrasonic.monitor(interval_ms=200)





