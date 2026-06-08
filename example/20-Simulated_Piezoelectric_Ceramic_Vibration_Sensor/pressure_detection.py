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

    应用场景：机柜防拆检测、设备跌落检测、门窗振动报警等。
    ADC 值越大表示振动/冲击越强。
    """

    def __init__(self, adc_channel=None, alert_threshold=1500):
        """初始化振动传感器实例。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            alert_threshold: 振动报警阈值，ADC 值超过此值触发报警，默认 1500
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.alert_threshold = alert_threshold
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_value(self):
        """读取当前振动强度 ADC 值。

        注意：值越大通常表示振动/冲击越强。

        Returns:
            int: ADC 采样值
        """
        return self.adc.read(self.adc_channel)

    def check_alert(self, value):
        """判断振动是否超过报警阈值。

        实际应用场景：机柜防拆检测、设备跌落检测、门窗振动报警等。

        Args:
            value: 当前 ADC 采样值

        Returns:
            bool: True 表示触发报警
        """
        return value >= self.alert_threshold

    def monitor(self, interval_ms=200):
        """后台监控循环，持续采样并输出振动状态。

        Args:
            interval_ms: 采样间隔，单位毫秒，默认 200ms
        """
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if self.check_alert(value):
                print("振动报警, 数值 = {}".format(value))
            else:
                print("振动数值 = {}".format(value))
            utime.sleep_ms(interval_ms)

    def start(self, interval_ms=200):
        """启动后台监控线程。

        Args:
            interval_ms: 采样间隔，单位毫秒，默认 200ms
        """
        self.open()
        _thread.start_new_thread(self.monitor, (interval_ms,))

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500)
    sensor.start()

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)
