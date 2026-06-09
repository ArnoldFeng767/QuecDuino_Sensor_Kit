"""
@file      : Inclination_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based inclination switch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class InclinationSwitch(object):
    """倾斜开关传感器类，通过 GPIO 检测倾斜状态并控制 LED 指示。

    应用场景：倾覆报警、设备姿态检测、运输振动指示等。
    """

    def __init__(self, pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU):
        """初始化倾斜开关传感器实例。

        Args:
            pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            led_pin: LED 指示灯 GPIO 引脚号，默认 GPIO32
            trigger_level: 触发电平，0 = 低电平触发，1 = 高电平触发，默认 0
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.gpio.read()

    def is_tilted(self):
        """判断当前是否处于倾斜状态。

        Returns:
            bool: True 表示已倾斜
        """
        return self.read_state() == self.trigger_level

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测倾斜状态并控制 LED。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            if self.is_tilted():
                self.led.write(1)
                print("检测到倾斜")
            else:
                self.led.write(0)
                print("水平状态")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    tilt_switch = InclinationSwitch(pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU)
    tilt_switch.monitor(interval_sec=1)