"""
@file      : flame.py
@author    : Aaron Chen
@brief     : Class-based flame sensor demo using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime


class FlameSensor(object):
    """Flame sensor packaging class."""

    def __init__(self, adc_channel=None,pin=Pin.GPIO31):
        self.adc = ADC()
        self.adc_channel = self.adc.ADC0 if adc_channel is None else adc_channel
        self.led=Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.is_running = False

    def open(self):
        self.adc.open()

    def read_value(self):
        return self.adc.read(self.adc_channel)

    def led_link(self):
        self.led.write(1)
        utime.sleep(0.5)
        self.led.write(0)
        utime.sleep(0.5)
    def monitor(self):
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            print(value)
            if value > 100 and value < 500:
                self.led.high()
                self.led.write(1)
                print("There is a fire hazard.")
            elif value > 500:
                self.led_link()
                print("There is a fire.")
            utime.sleep(1)

    def start(self):
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    flame_sensor = FlameSensor()
    flame_sensor.start()

    while True:
        utime.sleep_ms(1000)