"""
@file      : Finger_touch_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based finger touch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from machine import Pin
import utime


class TouchSensor(object):
    """人体触摸传感器类，通过 GPIO 检测触摸状态。

    典型用法:
        ts = TouchSensor(pin=Pin.GPIO31)
        ts.set_callback(lambda t: print("触摸!" if t else "释放"))
        ts.monitor()

    Args:
        pin:          传感器输入 GPIO，默认 GPIO31
        trigger_level: 触发电平，默认 1（高电平触发）
        pull:          上下拉配置，默认下拉 (Pin.PULL_PD)
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """设置触摸状态变化回调。callback(is_touched)"""
        self._callback = callback

    def read_state(self):
        """读取传感器当前电平状态。"""
        return self._gpio.read()

    def is_touched(self):
        """判断当前是否被触摸。"""
        return self.read_state() == self._trigger_level

    @property
    def trigger_count(self):
        """获取累计触摸次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触摸计数归零。"""
        self._trigger_count = 0

    def wait_for_touch(self, timeout_ms=None):
        """阻塞等待触摸。"""
        start = utime.ticks_ms()
        while True:
            if self.is_touched():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor(self, interval_sec=1):
        """轮询监控循环。"""
        while True:
            state = self.read_state()
            touched = state == self._trigger_level
            changed = touched != (self._last_state == self._trigger_level)
            self._last_state = state
            if changed:
                if touched:
                    self._trigger_count += 1
                if self._callback:
                    self._callback(touched)
                print("检测到触摸" if touched else "触摸释放")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    ts = TouchSensor(pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD)
    ts.monitor(interval_sec=1)
