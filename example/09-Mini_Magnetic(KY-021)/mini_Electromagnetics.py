"""
@file      : mini_Electromagnetics.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Mini Electromagnetics project using a mercury switch to detect magnetic field changes and control an output pin accordingly.
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""


from machine import Pin,ExtInt
import utime

# Global flag
human_detected = False

# Configure GPIO as input with pull-up functionality
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)
gpio1 = Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0)

def main():
    # When the sensor detects a magnetic field change, it outputs a low level (0).
    while True:
        if gpio.read() == 0:
            print("Magnetic field change detected")
            gpio1.write(1)
        else:
            print("No magnetic field change detected")
            gpio1.write(0)
        utime.sleep(1)
        

if __name__ == '__main__':
    main()