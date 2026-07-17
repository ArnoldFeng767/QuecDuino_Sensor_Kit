"""
@file      : pressure_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based vibration/impact detection using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
import _thread
import utime


class VibrationSensor(object):
    """振动传感器类，通过 ADC 采集振动强度并阈值报警。

    典型用法:
        sensor = VibrationSensor(alert_threshold=1500)
        sensor.set_callback(lambda val: print("振动!", val))
        sensor.start()

    Args:
        adc_channel:    ADC 通道，默认 ADC1
        alert_threshold: 报警阈值，默认 1500
        sample_ms:      采样间隔 ms，默认 200
    """

    def __init__(self, adc_channel=None, alert_threshold=1500, sample_ms=200):
        self._alert_threshold = alert_threshold
        self._sample_ms = sample_ms
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置振动报警回调。

        Args:
            callback: 回调函数，签名 callback(adc_value)
        """
        self._callback = callback

    # ---- 阈值 ----

    @property
    def alert_threshold(self):
        return self._alert_threshold

    @alert_threshold.setter
    def alert_threshold(self, value):
        self._alert_threshold = value

    # ---- 读取 ----

    def read_value(self):
        """读取当前振动强度 ADC 值。"""
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_alert(self, value=None):
        """判断振动是否超过报警阈值。

        Args:
            value: ADC 值，默认使用最近一次采样值

        Returns:
            bool: True 表示触发报警
        """
        v = value if value is not None else self._last_value
        return v >= self._alert_threshold

    # ---- 监控 ----

    def _monitor(self):
        """后台监控循环。"""
        while self._is_running:
            value = self.read_value()
            if value >= self._alert_threshold:
                print("振动报警, 数值 = {}".format(value))
                if self._callback:
                    self._callback(value)
            utime.sleep_ms(self._sample_ms)

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """停止后台监控线程。"""
        self._is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500, sample_ms=200)
    sensor.set_callback(lambda v: print("振动报警触发! ADC={}".format(v)))
    sensor.start()

    while True:
        utime.sleep_ms(1000)
