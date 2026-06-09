"""
@file      : Finger_touch_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based finger touch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class TouchSensor(object):
    """人体触摸传感器类，通过 GPIO 检测触摸状态。

    应用场景：触摸开关、人机交互、接近检测等。
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD):
        """初始化触摸传感器实例。

        Args:
            pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            trigger_level: 触发电平，默认 1（高电平触发）
            pull: 上下拉配置，默认下拉 (Pin.PULL_PD)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.trigger_level = trigger_level

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.gpio.read()

    def is_touched(self):
        """判断当前是否被触摸。

        Returns:
            bool: True 表示检测到触摸
        """
        return self.read_state() == self.trigger_level

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测触摸状态。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            if self.is_touched():
                print("检测到触摸")
            else:
                print("未检测到触摸")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    touch_sensor = TouchSensor(pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD)
    touch_sensor.monitor(interval_sec=1)
