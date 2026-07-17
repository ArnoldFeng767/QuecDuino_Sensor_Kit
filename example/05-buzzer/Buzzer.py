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

    典型用法:
        buzzer = ActiveBuzzer(pin=Pin.GPIO31, active_level=0)
        buzzer.beep(duration_ms=200)
        buzzer.beep_pattern([(200, 100), (500, 200), (200, 100)])

    Args:
        pin:          GPIO 引脚号，默认 GPIO31
        active_level: 触发电平，1=高电平触发，0=低电平触发，默认 1
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self._active_level = active_level
        self._inactive_level = 0 if active_level else 1
        self._gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self._inactive_level)
        self._state = 0  # 0=关闭, 1=鸣响

    # ---- 基础控制 ----

    def on(self):
        """开启蜂鸣器（输出触发电平）。"""
        self._state = 1
        self._gpio.write(self._active_level)

    def off(self):
        """关闭蜂鸣器（输出非触发电平）。"""
        self._state = 0
        self._gpio.write(self._inactive_level)

    def toggle(self):
        """翻转蜂鸣器状态（响→停，停→响）。"""
        self.off() if self._state else self.on()

    # ---- 状态 ----

    def is_on(self):
        """查询蜂鸣器当前是否在鸣响。

        Returns:
            bool: True 表示正在鸣响
        """
        return self._state == 1

    def read(self):
        """读取当前逻辑状态。

        Returns:
            int: 1=鸣响, 0=关闭
        """
        return self._state

    # ---- 鸣响 ----

    def beep(self, duration_ms=200):
        """蜂鸣器鸣响一次（阻塞）。

        Args:
            duration_ms: 鸣响持续时间，单位毫秒，默认 200ms
        """
        self.on()
        utime.sleep_ms(duration_ms)
        self.off()

    def beep_times(self, times=3, duration_ms=200, interval_ms=200):
        """蜂鸣器连续鸣响多次。

        Args:
            times:        鸣响次数，默认 3
            duration_ms:  每次鸣响持续时间，单位毫秒，默认 200ms
            interval_ms:  两次鸣响间隔，单位毫秒，默认 200ms
        """
        for _ in range(times):
            self.beep(duration_ms)
            utime.sleep_ms(interval_ms)

    def beep_pattern(self, pattern, repeat=1):
        """按自定义节奏模式鸣响。

        Args:
            pattern: [(on_ms, off_ms), ...] 节奏列表，每项为 (鸣响时长, 间隔时长)
            repeat:  重复次数，默认 1 次

        Example:
            # SOS 模式：三短三长三短
            buzzer.beep_pattern([(100,100), (100,100), (100,300),
                                 (300,100), (300,100), (300,300),
                                 (100,100), (100,100), (100,500)])
        """
        for _ in range(repeat):
            for on_ms, off_ms in pattern:
                self.on()
                utime.sleep_ms(on_ms)
                self.off()
                utime.sleep_ms(off_ms)


# ---- 独立运行测试 ----
if __name__ == '__main__':
    buzzer = ActiveBuzzer(pin=Pin.GPIO31, active_level=1)
    # 鸣响 3 次
    buzzer.beep_times(times=3, duration_ms=200, interval_ms=200)
    utime.sleep_ms(500)
    # 自定义节奏
    buzzer.beep_pattern([(100, 100), (300, 300), (100, 100)])
