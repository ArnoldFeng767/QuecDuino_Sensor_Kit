"""
@file      : MIC.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Microphone signal processing
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

    
if __name__=='__main__':
    LED=Pin(1,Pin.OUT,Pin.PULL_DISABLE,0)
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())
