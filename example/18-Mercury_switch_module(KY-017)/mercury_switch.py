"""
@file      : mercury_switch.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based mercury switch detection using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class MercurySwitch(object):
    """水银开关传感器类，检测倾斜状态并联动输出。

    应用场景：倾覆报警、跌落检测、防盗装置等。
    水银开关倾斜到一定角度时导通，输出触发电平。
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU):
        """初始化水银开关传感器实例。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.sensor = Pin(sensor_pin, Pin.IN, pull)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.sensor.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到倾斜）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_state() == self.trigger_level

    def update(self):
        """根据倾斜状态更新联动输出。"""
        if self.is_triggered():
            self.output.write(1)
            print("水银开关检测到倾斜")
        else:
            self.output.write(0)
            print("水银开关未检测到倾斜")

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测倾斜状态并联动输出。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            self.update()
            utime.sleep(interval_sec)


if __name__ == '__main__':
    mercury = MercurySwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU)
    mercury.monitor(interval_sec=1)
