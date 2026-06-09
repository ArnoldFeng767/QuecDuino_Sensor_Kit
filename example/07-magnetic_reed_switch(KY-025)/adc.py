"""
@file      : adc.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based magnetic reed switch detection using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from misc import ADC
from machine import Pin
import _thread
import utime


class MagneticReedSwitch(object):
    """磁簧开关传感器类（ADC 模式），通过模拟量读取磁场强度变化。

    应用场景：门窗防盗、智能计数、位置限位检测、无触点开关等。
    当 ADC 值超过阈值时判定为检测到磁场，点亮 LED 指示。
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, threshold=100):
        """初始化磁簧开关传感器实例（ADC 模式）。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            led_pin: LED 指示灯 GPIO 引脚号，默认 GPIO31
            threshold: 磁场强度阈值，ADC 值超过此值判定为检测到磁场，默认 100
        """
        self.threshold = threshold
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_value(self):
        """读取当前磁场强度的 ADC 值。

        Returns:
            int: ADC 采样值
        """
        return self.adc.read(self.adc_channel)

    def handle_magnetic_field(self, value):
        """根据磁场强度控制 LED 指示。

        超过阈值点亮 LED，低于阈值熄灭 LED。
        实际应用场景：门磁报警——磁铁靠近（门关）不亮灯，磁铁远离（门开）亮灯报警。

        Args:
            value: 当前 ADC 采样值
        """
        if value > self.threshold:
            self.led.write(1)
        else:
            self.led.write(0)

    def monitor(self):
        """后台监控循环，持续采样并输出磁场状态。"""
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            status = "检测到磁场" if value > self.threshold else "无磁场"
            print("ADC: {} | 状态: {}".format(value, status))
            self.handle_magnetic_field(value)
            utime.sleep_ms(500)

    def start(self):
        """启动后台采样线程。"""
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        """停止后台采样线程。"""
        self.is_running = False


if __name__ == '__main__':
    magnetic_reed_switch = MagneticReedSwitch(
        led_pin=Pin.GPIO31,
        threshold=100,
    )
    magnetic_reed_switch.start()

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)