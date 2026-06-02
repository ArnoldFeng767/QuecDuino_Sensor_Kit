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


def fun():
    while True:
        num=adc.read(adc.ADC1)
        utime.sleep(1)#A specific voltage value is obtained, and the duty cycle is controlled based on this voltage value.
        print(num)
        return num

def LED_SW(num):
    if num<50:
        LED.write(0)
        print("Light is strong, close led")
    else:
        LED.write(1)
        print("Light is weak, open led")

if __name__=='__main__':
    LED=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,0)
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())
    while True:
        num=fun()        
        LED_SW(num)
