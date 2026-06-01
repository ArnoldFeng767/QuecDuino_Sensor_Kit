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

# KY-032 引脚说明:
#   VCC: 3.3-5V
#   GND: 接地
#   OUT: 数字输出 (无障碍物=高电平1, 有障碍物=低电平0)
#   EN:  使能引脚 (可选，悬空默认使能)
# 注意: 模块上有两个电位器可调节检测距离和灵敏度

# 配置GPIO为输入，上拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

# ==================== 轮询模式 ====================
def main_polling():
    print("KY-032 obstacle avoidance sensor (polling mode)")
    while True:
        if gpio.read() == 0:
            print("检测到障碍物")
        else:
            print("无障碍物")
        utime.sleep_ms(200)

# ==================== 中断模式 ====================
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
            print("检测到障碍物")
            obstacle_flag = False
        else:
            print("无障碍物")
        utime.sleep_ms(200)


if __name__ == '__main__':
    main_polling()
    # main_interrupt()  # 切换为中断模式
