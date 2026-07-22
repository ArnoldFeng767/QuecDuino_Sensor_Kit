"""
@file      : led.py
@author    : Arnold Feng
@brief     : LED 驱动模块，支持高低电平自适应、开关、闪烁与翻转控制
@version   : 0.3
@date      : 2026-07-17
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class LED(object):
    """LED 驱动类，封装 GPIO 引脚对 LED 的基本操作。

    通过 active_level 参数适配不同硬件接法：
        - active_level=1：高电平点亮（默认，源极驱动 / 共阴极）
        - active_level=0：低电平点亮（漏极驱动 / 共阳极）

    典型用法:
        led = LED(Pin.GPIO31)
        led.on()
        led.blink(times=5, interval=0.5)

    Args:
        pin:  GPIO 引脚号，例如 Pin.GPIO31
        active_level: 点亮电平，1=高电平点亮，0=低电平点亮
    """

    def __init__(self, pin, active_level=1):
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)
        self.state = 0  # 0=灭, 1=亮（软件跟踪，与硬件电平解耦）

    # ---- 基础 IO ----

    def write(self, value):
        """设置 LED 的逻辑状态。

        Args:
            value: 1=点亮, 0=熄灭（与 active_level 无关的逻辑值）
        """
        self.state = value
        self.pin.write(self.active_level if value else self.inactive_level)

    def read(self):
        """读取 LED 当前的逻辑状态。

        Returns:
            int: 1=亮, 0=灭
        """
        return self.state

    # ---- 快捷操作 ----

    def on(self):
        """点亮 LED。"""
        self.write(1)

    def off(self):
        """熄灭 LED。"""
        self.write(0)

    def toggle(self):
        """翻转 LED 状态（亮→灭，灭→亮）。"""
        self.write(0 if self.state else 1)

    # ---- 闪烁 ----

    def blink(self, interval=0.5, times=None):
        """LED 闪烁，以指定间隔循环亮灭。

        Args:
            interval: 亮灭单边持续时间，单位秒，默认 0.5s
            times:    闪烁次数（亮+灭=1次），None 表示无限循环

        Example:
            led.blink(interval=0.2, times=3)   # 快闪 3 次后停止
            led.blink(interval=1.0)             # 每秒闪烁，无限循环
        """
        n = 0
        while times is None or n < times:
            self.on()
            utime.sleep(interval)
            self.off()
            utime.sleep(interval)
            n += 1


# ---- 独立运行测试 ----
if __name__ == '__main__':
    led = LED(Pin.GPIO31, active_level=1)
    # 快闪 3 次后常亮
    led.blink(interval=0.3, times=3)
    led.on()
    print("LED 测试完成：3 次闪烁后常亮")
