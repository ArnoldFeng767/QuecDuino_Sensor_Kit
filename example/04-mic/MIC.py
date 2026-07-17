"""
@file      : MIC.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based microphone signal processing example
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime


class Mic(object):
    """麦克风传感器类，通过 ADC 采集声音强度，支持阈值触发与回调通知。

    典型用法:
        mic = Mic(led_pin=Pin.GPIO31, threshold=200)
        mic.set_callback(lambda val: print("loud!", val))
        mic.start()

    Args:
        adc_channel: ADC 通道，默认 ADC1
        led_pin:     LED 指示 GPIO 引脚号，默认 GPIO31，传 None 禁用
        threshold:   声音强度阈值，超过触发，默认 200
        sample_ms:   采样间隔 ms，默认 500
        led_on_ms:   LED 点亮持续时间 ms，默认 500（非阻塞）
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 threshold=200, sample_ms=500, led_on_ms=500):
        self._threshold = threshold
        self._sample_ms = sample_ms
        self._led_on_ms = led_on_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0
        self._led_off_at = 0  # LED 熄灭时间戳

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置声音触发回调函数。

        Args:
            callback: 回调函数，签名 callback(value)，传 None 取消
        """
        self._callback = callback

    # ---- 阈值 ----

    @property
    def threshold(self):
        """当前触发阈值。"""
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        """运行时修改触发阈值。

        Args:
            value: 新的 ADC 阈值
        """
        self._threshold = value

    # ---- 读取 ----

    def read_value(self):
        """读取当前声音强度 ADC 值。

        Returns:
            int: ADC 采样值
        """
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_detected(self):
        """判断最近一次采样是否超过阈值。

        Returns:
            bool: True 表示检测到声音事件
        """
        return self._last_value > self._threshold

    # ---- LED（非阻塞） ----

    def _led_on(self):
        """点亮 LED（非阻塞）。"""
        if self._led is not None:
            self._led.write(1)
            self._led_off_at = utime.ticks_ms() + self._led_on_ms

    def _led_tick(self):
        """检查 LED 是否需要熄灭（由 monitor 循环调用）。"""
        if self._led is not None and self._led_off_at > 0:
            if utime.ticks_diff(utime.ticks_ms(), self._led_off_at) >= 0:
                self._led.write(0)
                self._led_off_at = 0

    # ---- 监控 ----

    def _monitor(self):
        """后台监控循环，非阻塞采样，支持回调与 LED 指示。"""
        while self._is_running:
            value = self.read_value()

            if value > self._threshold:
                self._led_on()
                if self._callback:
                    self._callback(value)

            self._led_tick()
            utime.sleep_ms(self._sample_ms)

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


# ---- 独立运行测试 ----
if __name__ == '__main__':
    def on_sound(value):
        print("检测到声音! ADC = {}".format(value))

    mic = Mic(led_pin=Pin.GPIO31, threshold=200, sample_ms=500, led_on_ms=500)
    mic.set_callback(on_sound)
    mic.start()

    while True:
        utime.sleep_ms(1000)
