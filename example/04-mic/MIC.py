"""
@file      : MIC.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based microphone signal processing example
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime


class Mic(object):
    """Microphone sensor packaging class."""

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, threshold=200):
        self.threshold = threshold
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def open(self):
        self.adc.open()

    def read_value(self):
        return self.adc.read(self.adc_channel)

    def handle_sound(self, value):
        if value > self.threshold:
            self.led.write(1)
            utime.sleep(2)
            self.led.write(0)

    def monitor(self):
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            print(value)
            self.handle_sound(value)
            utime.sleep_ms(500)

    def start(self):
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    mic = Mic(
        led_pin=Pin.GPIO31,
        threshold=200,
    )
    mic.start()

    while True:
        utime.sleep_ms(1000)
