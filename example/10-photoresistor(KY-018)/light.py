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

    传感器特性：光照越强，电阻越小，ADC 值越低；光照越弱，电阻越大，ADC 值越高。
    应用场景：自动路灯、智能照明、环境光检测等。
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, sample_ms=500):
        """初始化光敏电阻控制器。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            led_pin: LED 指示灯 GPIO 引脚号，默认 GPIO31
            sample_ms: 采样间隔，单位毫秒，默认 500ms
        """
        self.sample_ms = sample_ms
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self.adc.open()
        self.is_running = True
        _thread.start_new_thread(self.monitor, ())

    def monitor(self):
        """后台监控循环，读取光照强度并根据阈值控制 LED。

        注意：当前逻辑为演示用途（光线弱关灯，光线强开灯）。
        实际自动路灯场景应反转逻辑：光线弱 → 开灯，光线强 → 关灯。
        """
        while self.is_running:
            light_value = self.adc.read(self.adc_channel)
            print("光照强度值: {}".format(light_value))
            # 根据光照强度阈值控制 LED
            if light_value < 50:
                self.led.write(0)
                print("光线弱，关闭 LED")
            else:
                self.led.write(1)
                print("光线强，开启 LED")
            utime.sleep_ms(self.sample_ms)

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    light_controller = LightController(
        led_pin=Pin.GPIO31,
        sample_ms=500,
    )
    light_controller.start()

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)

