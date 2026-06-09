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
        - ADC < 100：无火焰
        - 100 <= ADC < 500：火险隐患，LED 常亮
        - ADC >= 500：火灾，LED 快闪

    应用场景：火灾预警、火源检测、安全监控等。
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31):
        """初始化火焰传感器实例（ADC 模式）。

        Args:
            adc_channel: ADC 通道，默认使用 ADC0
            led_pin: LED 报警指示灯 GPIO 引脚号，默认 GPIO31
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC0 if adc_channel is None else adc_channel
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_value(self):
        """读取当前火焰强度 ADC 值。

        Returns:
            int: ADC 采样值
        """
        return self.adc.read(self.adc_channel)

    def led_blink(self):
        """LED 快闪，用于火灾报警指示。"""
        self.led.write(1)
        utime.sleep(0.5)
        self.led.write(0)
        utime.sleep(0.5)

    def monitor(self):
        """后台监控循环，根据火焰强度分级响应。"""
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if value < 100:
                self.led.write(0)
                print("ADC: {} | 状态: 安全".format(value))
            elif value < 500:
                self.led.write(1)
                print("ADC: {} | 状态: 火险隐患".format(value))
            else:
                self.led_blink()
                print("ADC: {} | 状态: 火灾报警".format(value))
            utime.sleep(1)

    def start(self):
        """启动后台监控线程。"""
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    flame_sensor = FlameSensor()
    flame_sensor.start()

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)