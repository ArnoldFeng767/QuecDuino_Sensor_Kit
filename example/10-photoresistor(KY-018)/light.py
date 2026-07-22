"""
@file      : light.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : lamp control using ADC to read light intensity and control LED brightness
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2026
"""

from misc import ADC
from machine import Pin
import _thread
import utime


class LightController(object):
    """光敏电阻控制器类，通过 ADC 读取光照强度并控制 LED。

    传感器特性：光照越强，ADC 值越低；光照越弱，ADC 值越高。

    典型用法:
        # 自动路灯模式：暗时开灯
        lc = LightController(led_pin=Pin.GPIO31, dark_threshold=200, led_mode='dark')
        lc.start()

    Args:
        adc_channel:    ADC 通道，默认 ADC1
        led_pin:        LED 指示 GPIO，默认 GPIO31，传 None 禁用
        dark_threshold: 低于此值判定为暗，默认 200
        led_mode:       'dark'=暗时亮灯, 'bright'=亮时亮灯, 'off'=仅监控不控灯，默认 'bright'
        sample_ms:      采样间隔 ms，默认 500
    """

    MODE_DARK = 'dark'      # 暗时开灯（自动路灯）
    MODE_BRIGHT = 'bright'  # 亮时开灯（演示模式）
    MODE_OFF = 'off'        # 不控制 LED

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 dark_threshold=200, led_mode='bright', sample_ms=500):
        self._dark_threshold = dark_threshold
        self._led_mode = led_mode
        self._sample_ms = sample_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置光照变化回调。

        Args:
            callback: 回调函数，签名 callback(adc_value, is_dark)
        """
        self._callback = callback

    # ---- 阈值 ----

    @property
    def dark_threshold(self):
        return self._dark_threshold

    @dark_threshold.setter
    def dark_threshold(self, value):
        self._dark_threshold = value

    # ---- 读取 ----

    def read_value(self):
        """读取当前光照强度 ADC 值。

        Returns:
            int: ADC 采样值
        """
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_dark(self):
        """判断当前环境是否偏暗。

        Returns:
            bool: True 表示暗
        """
        return self._last_value > self._dark_threshold

    # ---- LED ----

    def _update_led(self, value):
        """根据 led_mode 更新 LED 状态。"""
        if self._led is None or self._led_mode == self.MODE_OFF:
            return
        dark = value > self._dark_threshold

        if self._led_mode == self.MODE_DARK:
            self._led.write(1 if dark else 0)
        elif self._led_mode == self.MODE_BRIGHT:
            self._led.write(0 if dark else 1)

    # ---- 监控 ----

    def _monitor(self):
        """后台监控循环。"""
        while self._is_running:
            value = self.read_value()
            dark = self.is_dark()
            self._update_led(value)
            print("光照: {} | {}".format(value, "暗" if dark else "亮"))

            if self._callback:
                self._callback(value, dark)

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
    lc = LightController(led_pin=Pin.GPIO31, dark_threshold=200,
                         led_mode=LightController.MODE_DARK, sample_ms=500)
    lc.start()

    while True:
        utime.sleep_ms(1000)
