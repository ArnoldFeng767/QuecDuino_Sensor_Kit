"""
@file      : Inclination_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Inclination switch detection using GPIO interrupt
@version   : 0.1
@date      : 2026-04-22
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


# Configure GPIO as input with pull-up
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)


def main():
    # Assuming that the sensor detects an inclination, it outputs a low level (0).
    while True:
        if gpio.read() == 0:
            print("Tilt detected")
        else:
            print("Level state")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()