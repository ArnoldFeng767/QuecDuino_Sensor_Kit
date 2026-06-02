"""
@file      : obstacle_avoidance.py
@author    : Aaron Chen
@brief     : KY-032 infrared obstacle avoidance sensor driver
@version   : 0.2
@date      : 2026-04-10
@copyright : Copyright (c) 2026
"""

from machine import Pin, ExtInt
import utime

# KY-032 Pin Description:
#   VCC: 3.3-5V
#   GND: Ground
#   OUT: Digital Output (No Obstacle = High Level 1, Obstacle Present = Low Level 0)
#   EN: Enable Pin (Optional, Default Enabled when left unconnected)
# Note: There are two potentiometers on the module that can be adjusted to control the detection distance and sensitivity.

# Configure GPIO as input with pull-up functionality
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

# ==================== Polling Mode ====================
def main_polling():
    print("KY-032 obstacle avoidance sensor (polling mode)")
    while True:
        if gpio.read() == 0:
            print("Obstacle detected")
        else:
            print("No obstacle")
        utime.sleep_ms(200)

# ==================== Interrupt Mode ====================
obstacle_flag = False

def irq_handler(args):
    global obstacle_flag
    if gpio.read() == 0:
        obstacle_flag = True

def main_interrupt():
    global obstacle_flag
    ext = ExtInt(ExtInt.GPIO31, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, irq_handler)
    ext.enable()
    print("KY-032 obstacle avoidance sensor (interrupt mode)")
    while True:
        if obstacle_flag:
            print("Obstacle detected")
            obstacle_flag = False
        else:
            print("No obstacle")
        utime.sleep_ms(200)


if __name__ == '__main__':
    main_polling()
    # main_interrupt()  # Switch to interrupt mode
