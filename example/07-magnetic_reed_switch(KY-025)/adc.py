"""
@file      : adc.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based magnetic reed switch detection using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from misc import ADC
from machine import Pin
import _thread
import utime

class MagneticReedSwitch(object):
    """Magnetic reed switch sensor packaging class."""

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, threshold=100):
        self.threshold = threshold
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def open(self):
        self.adc.open()

    def read_value(self):
        return self.adc.read(self.adc_channel)

    
    def handle_magnetic_field(self, value):
        if value > self.threshold:
            self.led.write(1)
        else:
            self.led.write(0)

    def monitor(self):
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            print(value)
            self.handle_magnetic_field(value)
            utime.sleep_ms(500) 

    def start(self):
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    magnetic_reed_switch = MagneticReedSwitch(
        led_pin=Pin.GPIO31,
        threshold=100,
    )
    magnetic_reed_switch.start()

    while True:
        utime.sleep_ms(1000)