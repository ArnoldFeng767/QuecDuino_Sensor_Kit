"""
@file      : Laser_emitter.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based laser emitter control using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class LaserEmitter(object):
    """激光发射器控制类，通过 GPIO 控制激光开关和闪烁。

    通过 active_level 参数适配不同触发方式。
    应用场景：激光指示、对准辅助、安防警示等。
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        """初始化激光发射器实例。

        Args:
            pin: GPIO 引脚号，默认 GPIO31
            active_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
        """
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        """开启激光。"""
        self.gpio.write(self.active_level)
        print("激光开启")

    def off(self):
        """关闭激光。"""
        self.gpio.write(self.inactive_level)
        print("激光关闭")

    def blink(self, interval=2):
        """激光闪烁一次（开→关）。

        Args:
            interval: 开关间隔，单位秒，默认 2 秒
        """
        self.on()
        utime.sleep(interval)
        self.off()
        utime.sleep(interval)

    def demo(self, interval=2):
        """演示循环，持续闪烁。

        Args:
            interval: 闪烁间隔，单位秒，默认 2 秒
        """
        while True:
            self.blink(interval)


if __name__ == '__main__':
    laser = LaserEmitter(pin=Pin.GPIO31, active_level=1)
    laser.demo(interval=2)
