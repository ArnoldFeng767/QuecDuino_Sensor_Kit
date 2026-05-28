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
        utime.sleep(1)#出现具体电压值，通过电压值控制占空比
        print(num)
        return num

def LED_SW(num):
    if num<50:
        LED.write(1)
        print("光线较强")
    else:
        LED.write(0)
        print("光线较弱")

if __name__=='__main__':
    LED=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,0)
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())
    while True:
        num=fun()        
        LED_SW(num)
