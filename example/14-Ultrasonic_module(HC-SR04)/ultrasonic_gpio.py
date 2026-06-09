"""
@file      : ultrasonic_gpio.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based ultrasonic distance measurement using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class UltrasonicSensor(object):
    """超声波测距传感器类（HC-SR04），通过 Trig/Echo 引脚测量距离。

    测距原理：Trig 发送 >=10us 高电平触发，Echo 返回高电平脉冲宽度
    对应声波往返时间，距离 = 脉冲宽度(us) / 58.0（单位 cm）。

    内置滑动窗口滤波，减少单次测量误差。

    应用场景：智能小车避障、倒车雷达、液位测量、距离检测等。
    """

    def __init__(self, trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5):
        """初始化超声波传感器实例。

        Args:
            trig_pin: 触发引脚 GPIO 号，默认 GPIO30
            echo_pin: 回波引脚 GPIO 号，默认 GPIO31
            filter_size: 滑动窗口滤波大小，默认 5 次均值
        """
        self.trig = Pin(trig_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.echo = Pin(echo_pin, Pin.IN, Pin.PULL_DISABLE, 0)
        self.filter_size = filter_size
        self.dist_list = []

    def _trigger(self):
        """发送触发信号，Trig 拉高 >=10us 后拉低。"""
        self.trig.off()
        utime.sleep_us(2)
        self.trig.on()
        utime.sleep_us(10)
        self.trig.off()

    def read_distance(self):
        """读取单次测距值，带超时保护。

        Returns:
            float or None: 距离（cm），超时或信号异常时返回 None
        """
        self._trigger()

        # 等待 Echo 拉高（超时保护）
        t_out = 0
        while self.echo.value() == 0 and t_out < 30000:
            t_out += 1
        if t_out >= 30000:
            return None

        start = utime.ticks_us()

        # 等待 Echo 拉低，记录高电平持续时间（超时保护）
        t_out = 0
        while self.echo.value() == 1 and t_out < 500000:
            t_out += 1
        if t_out >= 500000:
            return None

        end = utime.ticks_us()
        duration = end - start
        # 声速 340m/s，距离 = 时间 / 58.0（cm）
        distance = duration / 58.0
        return round(distance, 2)

    def read_filtered_distance(self):
        """读取滤波后的距离值（滑动窗口均值）。

        有效测量范围：2cm ~ 800cm，超出范围的值被过滤。

        Returns:
            float or None: 滤波后距离（cm），无效时返回 None
        """
        raw_dist = self.read_distance()
        if raw_dist is None or not 2 <= raw_dist <= 800:
            return None

        self.dist_list.append(raw_dist)
        if len(self.dist_list) > self.filter_size:
            self.dist_list.pop(0)
        return round(sum(self.dist_list) / len(self.dist_list), 2)

    def monitor(self, interval_ms=200):
        """轮询监控循环，持续测量并输出距离。

        Args:
            interval_ms: 测量间隔，单位毫秒，默认 200ms
        """
        while True:
            avg_dist = self.read_filtered_distance()
            if avg_dist is not None:
                print("当前距离: {} cm".format(avg_dist))
            else:
                print("超出量程或信号异常")
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    ultrasonic = UltrasonicSensor(trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5)
    ultrasonic.monitor(interval_ms=200)





