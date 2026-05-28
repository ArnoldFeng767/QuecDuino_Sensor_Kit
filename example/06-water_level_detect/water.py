
"""
@file      : water.py
@author    : Aaron Chen
@brief     : Water level sensor demo using ADC
@version   : 0.1
@date      : 2026-04-10
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime

def fun():
    while True:
        num=adc.read(adc.ADC1)
        utime.sleep(1)
        print(num)

    
if __name__=='__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())