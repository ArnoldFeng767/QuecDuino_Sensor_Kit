"""
@file      : light.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : lamp control using ADC to read light intensity and control LED brightness
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime

class LightController(object):
    """Light sensor control class using ADC to read light intensity and control LED brightness."""

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31):

        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def start(self):
        self.adc.open()
        self.is_running = True
        _thread.start_new_thread(self.monitor, ())
        
    def monitor(self):
        while self.is_running:
            light_value = self.adc.read(self.adc_channel)
            print("Light intensity value:", light_value)
            # Control LED brightness based on light intensity (simple threshold control)
            if light_value < 50:  # Adjust threshold as needed
                self.led.write(0)  # Turn off LED
                print("Light is weak, turn off LED")
            else:
                self.led.write(1)  # Turn on LED
                print("Light is strong, turn on LED")
            utime.sleep_ms(500)

    def stop(self):
        self.is_running = False 

if __name__ == '__main__':
    light_controller = LightController(
        led_pin=Pin.GPIO31,
    )
    light_controller.start()

    while True:
        utime.sleep_ms(1000)

