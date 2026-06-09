"""
@file      : Magic_Halo.py
@author    : Aaron Chen
@brief     : Simple class-based tilt sensor example
@version   : 0.1
@date      : 2026-06-02
"""

from machine import Pin
import utime


class TiltSwitch(object):
    """倾斜开关传感器类，检测设备姿态并联动输出。

    应用场景：倾覆报警、设备姿态检测、运输振动/偏转指示等。
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        """初始化倾斜开关传感器实例。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
        """
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.sensor.read()

    def is_tilted(self):
        """判断当前是否处于倾斜状态。

        Returns:
            bool: True 表示已倾斜
        """
        return self.read_state() == self.trigger_level

    def update(self):
        """根据倾斜状态更新联动输出。"""
        if self.is_tilted():
            self.output.write(1)
            print("检测到倾斜")
        else:
            self.output.write(0)
            print("位置正常")

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测倾斜状态并联动输出。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            self.update()
            utime.sleep(interval_sec)


if __name__ == '__main__':
    tilt_switch = TiltSwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    tilt_switch.monitor(interval_sec=1)

