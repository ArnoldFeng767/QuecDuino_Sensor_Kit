"""
@file      : flame.py
@author    : Aaron Chen
@brief     : Class-based flame sensor demo using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime


class FlameSensor(object):
    """火焰传感器类（ADC 模式），通过模拟量读取火焰强度并分级报警。

    分级逻辑：
        - ADC < warn_threshold： 安全
        - warn_threshold <= ADC < alert_threshold： 火险隐患
        - ADC >= alert_threshold： 火灾报警

    典型用法:
        sensor = FlameSensor(led_pin=Pin.GPIO31)
        sensor.set_callback(lambda val, lvl: print("火警!" if lvl==2 else ""))
        sensor.start()

    Args:
        adc_channel:     ADC 通道，默认 ADC0
        led_pin:         LED 报警 GPIO，默认 GPIO31，传 None 禁用
        warn_threshold:  火险隐患阈值，默认 100
        alert_threshold: 火灾报警阈值，默认 500
    """

    LEVEL_SAFE = 0
    LEVEL_WARN = 1
    LEVEL_ALERT = 2

    _LEVEL_LABELS = {0: "安全", 1: "火险隐患", 2: "火灾报警"}

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 warn_threshold=100, alert_threshold=500):
        self._warn_threshold = warn_threshold
        self._alert_threshold = alert_threshold
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC0 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0
        self._last_level = self.LEVEL_SAFE

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置火焰检测回调。

        Args:
            callback: 回调函数，签名 callback(adc_value, level)
        """
        self._callback = callback

    # ---- 读取 ----

    def read_value(self):
        """读取当前火焰强度 ADC 值。

        Returns:
            int: ADC 采样值
        """
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def check_level(self, value):
        """根据 ADC 值判断报警等级。

        Args:
            value: ADC 采样值

        Returns:
            int: LEVEL_SAFE / LEVEL_WARN / LEVEL_ALERT
        """
        if value < self._warn_threshold:
            return self.LEVEL_SAFE
        elif value < self._alert_threshold:
            return self.LEVEL_WARN
        else:
            return self.LEVEL_ALERT

    @classmethod
    def level_label(cls, level):
        """获取等级标签。"""
        return cls._LEVEL_LABELS.get(level, "未知")

    # ---- LED（非阻塞） ----

    def _update_led(self, level):
        if self._led is None:
            return
        if level == self.LEVEL_SAFE:
            self._led.write(0)
        elif level == self.LEVEL_WARN:
            self._led.write(1)
        # LEVEL_ALERT: LED 快闪在 _monitor 里处理

    # ---- 监控 ----

    def _monitor(self):
        """后台监控循环，根据火焰强度分级响应。"""
        blink_state = 0
        last_blink = 0
        while self._is_running:
            value = self.read_value()
            level = self.check_level(value)
            self._last_level = level

            label = self.level_label(level)
            print("ADC: {} | 状态: {}".format(value, label))

            if level == self.LEVEL_ALERT:
                # LED 快闪（非阻塞）
                now = utime.ticks_ms()
                if utime.ticks_diff(now, last_blink) >= 250:
                    blink_state = 0 if blink_state else 1
                    if self._led:
                        self._led.write(blink_state)
                    last_blink = now
            else:
                self._update_led(level)

            if self._callback:
                self._callback(value, level)

            utime.sleep_ms(200)

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """停止后台监控线程并关闭 LED。"""
        self._is_running = False
        if self._led is not None:
            self._led.write(0)


if __name__ == '__main__':
    sensor = FlameSensor()
    sensor.set_callback(lambda v, l: print("!!!" if l == 2 else ""))
    sensor.start()

    while True:
        utime.sleep_ms(1000)
