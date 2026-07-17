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

    典型用法:
        sensor = UltrasonicSensor(trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31)
        dist = sensor.read_filtered_distance()
        sensor.monitor()

    Args:
        trig_pin:   触发引脚 GPIO，默认 GPIO30
        echo_pin:   回波引脚 GPIO，默认 GPIO31
        filter_size: 滑动窗口大小，默认 5
    """

    def __init__(self, trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5):
        self._trig = Pin(trig_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._echo = Pin(echo_pin, Pin.IN, Pin.PULL_DISABLE, 0)
        self._filter_size = filter_size
        self._dist_list = []
        self._callback = None
        self._last_distance = None

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置测距回调。

        Args:
            callback: 回调函数，签名 callback(distance_cm)
        """
        self._callback = callback

    # ---- 测量 ----

    @property
    def last_distance(self):
        """最近一次有效测距值 cm。"""
        return self._last_distance

    def _trigger(self):
        """发送触发信号，Trig 拉高 >=10us 后拉低。"""
        self._trig.off()
        utime.sleep_us(2)
        self._trig.on()
        utime.sleep_us(10)
        self._trig.off()

    def read_distance(self):
        """读取单次测距值，带超时保护。

        Returns:
            float or None: 距离（cm），超时或信号异常时返回 None
        """
        self._trigger()

        t_out = 0
        while self._echo.value() == 0 and t_out < 30000:
            t_out += 1
        if t_out >= 30000:
            return None

        start = utime.ticks_us()

        t_out = 0
        while self._echo.value() == 1 and t_out < 500000:
            t_out += 1
        if t_out >= 500000:
            return None

        end = utime.ticks_us()
        duration = end - start
        distance = duration / 58.0
        return round(distance, 2)

    def read_filtered_distance(self):
        """读取滤波后的距离值（滑动窗口均值）。

        有效测量范围：2cm ~ 800cm。

        Returns:
            float or None: 滤波后距离（cm），无效时返回 None
        """
        raw_dist = self.read_distance()
        if raw_dist is None or not 2 <= raw_dist <= 800:
            return None

        self._dist_list.append(raw_dist)
        if len(self._dist_list) > self._filter_size:
            self._dist_list.pop(0)
        result = round(sum(self._dist_list) / len(self._dist_list), 2)
        self._last_distance = result
        return result

    # ---- 监控 ----

    def monitor(self, interval_ms=200):
        """轮询监控循环，持续测量并输出距离。

        Args:
            interval_ms: 测量间隔 ms，默认 200
        """
        while True:
            avg_dist = self.read_filtered_distance()
            if avg_dist is not None:
                print("当前距离: {} cm".format(avg_dist))
                if self._callback:
                    self._callback(avg_dist)
            else:
                print("超出量程或信号异常")
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    ultrasonic = UltrasonicSensor(trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5)
    ultrasonic.monitor(interval_ms=200)
