"""
@file      : Laser_emitter.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based laser emitter control using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime

class LaserEmitter:
    """Laser emission module packaging class."""

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        self.gpio.write(self.active_level)
        print("laser on")

    def off(self):
        self.gpio.write(self.inactive_level)
        print("laser off")

    def blink(self,):
        self.on()
        utime.sleep(2)
        self.off()
        utime.sleep(2)

    def demo(self):
        while True:
            self.blink()


if __name__ == '__main__':
    laser = LaserEmitter(pin=Pin.GPIO31, active_level=1)
    laser.demo()
        
        
        
        
        
        
        
        
        
        