"""
@file      : mini_Electromagnetics.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based mini magnetic sensor project with output linkage control.
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class MiniMagneticController(object):
    """迷你磁簧传感器控制类，磁场检测 + 输出联动控制。

    应用场景：门磁触发后联动输出，驱动告警灯、蜂鸣器或继电器。
    例如门禁状态指示、入侵检测、开盖报警等。
    """

    def __init__(
        self,
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    ):
        """初始化磁簧传感器控制器。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，0 = 低电平触发，1 = 高电平触发，默认 0
            output_active_level: 输出激活电平，默认 1（高电平激活）
        """
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PU)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.output_active_level = output_active_level
        self.output_inactive_level = 0 if output_active_level else 1
        self.last_state = self.sensor.read()

    def read_sensor(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.sensor.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到磁场）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_sensor() == self.trigger_level

    def set_output(self, active):
        """控制联动输出引脚电平。

        可用于驱动 LED、蜂鸣器、继电器等外设。

        Args:
            active: True 激活输出，False 关闭输出
        """
        level = self.output_active_level if active else self.output_inactive_level
        self.output.write(level)

    def update(self):
        """根据传感器状态更新联动输出，并返回状态变化信息。

        Returns:
            tuple: (是否变化, 是否触发)
        """
        state = self.read_sensor()
        triggered = state == self.trigger_level
        self.set_output(triggered)

        if triggered:
            print("检测到磁场变化")
        else:
            print("未检测到磁场变化")

        changed = state != self.last_state
        self.last_state = state
        return changed, triggered

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测磁场状态并联动输出。

        实际应用场景：门禁状态指示和入侵检测等。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            changed, triggered = self.update()
            if changed:
                if triggered:
                    print("[MiniMagnetic] 触发事件")
                else:
                    print("[MiniMagnetic] 释放事件")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    controller = MiniMagneticController(
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    )
    controller.monitor()