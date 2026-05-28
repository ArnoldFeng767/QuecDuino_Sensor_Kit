"""
@file      : Buzzer.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Buzzer control using GPIO
@version   : 0.1
@date      : 2026-04-17
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime
gpio=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,0)
for _ in range(50):
    gpio.write(1)
    utime.sleep_ms(100)
    gpio.write(0)
    utime.sleep_ms(100)