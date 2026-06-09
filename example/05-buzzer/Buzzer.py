"""
@file      : Buzzer.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Active and passive buzzer driver classes
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class ActiveBuzzer(object):
    """有源蜂鸣器驱动类，内部自带振荡源，给定电平即可发声。

    通过 active_level 参数适配不同触发方式：
        - active_level=1：高电平触发（默认）
        - active_level=0：低电平触发（本模块硬件为低电平触发）
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        """初始化有源蜂鸣器实例。

        Args:
            pin: GPIO 引脚号，默认 GPIO31
            active_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
        """
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        """开启蜂鸣器（输出触发电平）。"""
        self.gpio.write(self.active_level)

    def off(self):
        """关闭蜂鸣器（输出非触发电平）。"""
        self.gpio.write(self.inactive_level)

    def beep(self, duration_ms=200):
        """蜂鸣器鸣响一次。

        Args:
            duration_ms: 鸣响持续时间，单位毫秒，默认 200ms
        """
        self.on()
        utime.sleep_ms(duration_ms)
        self.off()

    def beep_times(self, times=3, duration_ms=200, interval_ms=200):
        """蜂鸣器连续鸣响多次。

        Args:
            times: 鸣响次数，默认 3 次
            duration_ms: 每次鸣响持续时间，单位毫秒，默认 200ms
            interval_ms: 两次鸣响间隔，单位毫秒，默认 200ms
        """
        for _ in range(times):
            self.beep(duration_ms)
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    # 有源蜂鸣器模块为低电平触发，active_level 设为 0
    active_buzzer = ActiveBuzzer(pin=Pin.GPIO31, active_level=1)
    # 连续鸣响 15 次，每次 300ms，间隔 300ms
    active_buzzer.beep_times(times=15, duration_ms=300, interval_ms=300)
    utime.sleep_ms(1000)
 