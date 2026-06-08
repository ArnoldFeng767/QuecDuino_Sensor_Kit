"""
@file      : led.py
@author    : Arnold Feng
@brief     : LED 控制模块，支持开关、读写和闪烁测试
@version   : 0.2
@date      : 2026-06-08
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class LED(object):
    """LED 控制类，封装 GPIO 引脚对 LED 的基本操作。

    Args:
        pin: GPIO 引脚号，例如 Pin.GPIO31
    """

    def __init__(self, pin):
        # 初始化 GPIO 为输出模式，禁用上下拉电阻，默认低电平（LED 熄灭）
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)

    def write(self, value):
        """设置 LED 的电平状态。

        Args:
            value: 1 表示高电平（点亮），0 表示低电平（熄灭）
        """
        self.pin.write(value)

    def read(self):
        """读取当前 LED 引脚的电平状态。

        Returns:
            int: 1 或 0
        """
        return self.pin.read()

    def on(self):
        """点亮 LED（输出高电平）。"""
        self.pin.write(1)

    def off(self):
        """熄灭 LED（输出低电平）。"""
        self.pin.write(0)

    def blink(self, interval=1):
        """LED 闪烁，以指定间隔循环亮灭。

        Args:
            interval: 亮灭切换间隔，单位秒，默认 1 秒
        """
        while True:
            self.on()
            utime.sleep(interval)
            self.off()
            utime.sleep(interval)


if __name__ == '__main__':
    # 使用 GPIO31 引脚创建 LED 实例
    led = LED(Pin.GPIO31)
    # 运行闪烁测试（每秒切换一次）
    led.blink()
        