"""
@file      : key_ExtInt.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Key interrupt handling using GPIO 
@version   : 0.1
@date      : 2026-04-18
@copyright : Copyright (c) 2026
"""


from machine import ExtInt
def fun(args):
    print('### interrupt  {} ###'.format(args)) # args[0]:gpio号 args[1]:上升沿或下降沿

extint = ExtInt(ExtInt.GPIO31, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, fun, filter_time=50)#使能滤波，滤波时间为50ms

extint.enable() #使能中断