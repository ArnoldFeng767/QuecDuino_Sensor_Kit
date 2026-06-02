"""
@file      : Finger_touch_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Finger touch detection using GPIO interrupt
@version   : 0.1
@date      : 2026-04-22
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


# Configure the GPIO as an input with a pull-down resistor.
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PD)


def main():
    # When the sensor detects a touch, it outputs a high level (1)
    while True:
        if gpio.read() == 1:
            print("Touch detected")
        else:
            print("No touch detected")
        utime.sleep(1)
        

if __name__ == '__main__':
    main()