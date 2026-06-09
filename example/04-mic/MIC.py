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
    """麦克风传感器类，通过 ADC 采集声音强度，超过阈值时点亮 LED 提示。

    使用多线程在后台循环采样，主线程不会被阻塞。
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, threshold=200, sample_ms=500, led_on_sec=2):
        """初始化麦克风实例。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            led_pin: LED 指示灯 GPIO 引脚号，默认 GPIO31
            threshold: 声音强度阈值，超过此值触发 LED，默认 200
            sample_ms: 采样间隔，单位毫秒，默认 500ms
            led_on_sec: LED 点亮持续时间，单位秒，默认 2 秒
        """
        self.threshold = threshold
        self.sample_ms = sample_ms
        self.led_on_sec = led_on_sec
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_value(self):
        """读取当前声音强度的 ADC 值。

        Returns:
            int: ADC 采样值
        """
        return self.adc.read(self.adc_channel)

    def handle_sound(self, value):
        """处理声音检测，超过阈值时点亮 LED。

        注意：LED 点亮期间会阻塞当前线程（led_on_sec 秒）。

        Args:
            value: 当前 ADC 采样值
        """
        if value > self.threshold:
            self.led.write(1)
            utime.sleep(self.led_on_sec)
            self.led.write(0)

    def monitor(self):
        """后台监控循环，持续采样并处理声音事件。"""
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            print(value)
            self.handle_sound(value)
            utime.sleep_ms(self.sample_ms)

    def start(self):
        """启动后台采样线程。"""
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        """停止后台采样线程。"""
        self.is_running = False


if __name__ == '__main__':
    mic = Mic(
        led_pin=Pin.GPIO31,
        threshold=200,
        sample_ms=500,
        led_on_sec=2,
    )
    mic.start()

    # 主线程保持运行，等待后台采样
    while True:
        utime.sleep_ms(1000)
