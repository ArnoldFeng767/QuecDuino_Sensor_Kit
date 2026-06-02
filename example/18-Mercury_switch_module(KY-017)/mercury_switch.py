"""
@file      : mercury_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Mercury switch detection using GPIO
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime

# Global flag
human_detected = False

# Configure GPIO as input with pull-up
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)

def main():
    # Assume the sensor outputs a high level (1) when detecting tilt
    while True:
        if gpio.read() == 1:
            gpio1.write(1)
            print("Mercury detected inclination")
        else:
            gpio1.write(0)
            print("Mercury did not detect inclination")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()
