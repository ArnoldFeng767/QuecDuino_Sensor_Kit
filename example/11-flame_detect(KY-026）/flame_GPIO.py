"""
@file      : flame.py
@author    : Aaron Chen
@brief     : Class-based flame sensor demo using GPIO.
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class FlameDigitalSensor(object):
    """火焰传感器类（GPIO 模式），通过数字量检测火焰并联动输出。

    应用场景：火灾报警、火源检测、安全监控等。
    检测到火焰时触发输出，可驱动 LED、蜂鸣器等报警设备。
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        """初始化火焰传感器实例（GPIO 模式）。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
        """
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.last_state = self.sensor.read()

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.sensor.read()

    def is_flame_detected(self):
        """判断当前是否检测到火焰。

        Returns:
            bool: True 表示检测到火焰
        """
        return self.read_state() == self.trigger_level

    def set_output(self, active):
        """控制联动输出引脚，可驱动 LED、蜂鸣器等。

        Args:
            active: True 激活输出，False 关闭输出
        """
        self.output.write(1 if active else 0)

    def update(self):
        """根据传感器状态更新联动输出，并返回状态变化信息。

        Returns:
            tuple: (是否变化, 是否检测到火焰)
        """
        state = self.read_state()
        detected = state == self.trigger_level
        self.set_output(detected)

        if detected:
            print("检测到火焰")

        changed = state != self.last_state
        self.last_state = state
        return changed, detected

    def monitor(self, interval_ms=100):
        """轮询监控循环，检测火焰状态并联动输出。

        Args:
            interval_ms: 轮询间隔，单位毫秒，默认 100ms
        """
        while True:
            self.update()
            utime.sleep_ms(interval_ms)


if __name__ == "__main__":
    flame_sensor = FlameDigitalSensor(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    flame_sensor.monitor()
        