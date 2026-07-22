"""
@file      : Display_LCD.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based digital tube display control using GPIO
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class DigitalTubeDisplay(object):
    """8 段数码管显示类，通过 8 个 GPIO 引脚控制段码显示数字 0-9。

    段码编码（共阳极，0 = 点亮，1 = 熄灭）：
        索引顺序: [a, b, c, d, e, f, g, dp]

    典型用法:
        display = DigitalTubeDisplay()
        display.show(5)
        display.countdown(10)

    Args:
        auto_clear: 每次显示前自动清除，默认 True
    """

    # 数字 0-9 的段码表（共阳极反逻辑）
    _NUM_TABLE = [
        [0, 0, 0, 0, 1, 0, 0, 0],  # 0
        [0, 1, 0, 1, 1, 0, 1, 1],  # 1
        [1, 0, 0, 0, 0, 0, 0, 1],  # 2
        [0, 0, 0, 0, 0, 0, 1, 1],  # 3
        [0, 1, 0, 1, 0, 0, 1, 0],  # 4
        [0, 0, 1, 0, 0, 0, 1, 0],  # 5
        [0, 0, 1, 0, 0, 0, 0, 0],  # 6
        [0, 0, 0, 1, 1, 0, 1, 1],  # 7
        [0, 0, 0, 0, 0, 0, 0, 0],  # 8
        [0, 0, 0, 0, 0, 0, 1, 0],  # 9
    ]

    def __init__(self, auto_clear=True):
        self._auto_clear = auto_clear
        self._segments = [
            Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 1),  # a
            Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1),  # b
            Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 1),  # c
            Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1),  # d
            Pin(Pin.GPIO2,  Pin.OUT, Pin.PULL_DISABLE, 1),  # e
            Pin(Pin.GPIO3,  Pin.OUT, Pin.PULL_DISABLE, 1),  # f
            Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1),  # g
            Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 1),  # dp
        ]
        self._current = None

    # ---- 显示 ----

    def show(self, number):
        """显示指定数字（0-9），超出范围自动忽略。

        Args:
            number: 要显示的数字，范围 0-9
        """
        if number < 0 or number > 9:
            return
        self._current = number
        values = self._NUM_TABLE[number]
        for seg, val in zip(self._segments, values):
            seg.write(val)

    def clear(self):
        """清除显示（所有段熄灭）。"""
        self._current = None
        for seg in self._segments:
            seg.write(1)

    @property
    def current(self):
        """当前显示的数字，None 表示已清除。"""
        return self._current

    # ---- 效果 ----

    def countdown(self, start=9, end=0, interval_sec=1):
        """倒计时显示。

        Args:
            start:        起始数字，默认 9
            end:          结束数字，默认 0
            interval_sec: 间隔秒，默认 1
        """
        step = -1 if start > end else 1
        for n in range(start, end + step, step):
            self.show(n)
            utime.sleep(interval_sec)

    def demo(self, interval_sec=1):
        """演示循环，依次显示 0-9。

        Args:
            interval_sec: 间隔秒，默认 1
        """
        while True:
            for n in range(10):
                self.show(n)
                utime.sleep(interval_sec)


if __name__ == '__main__':
    display = DigitalTubeDisplay()
    display.countdown(9, 0, interval_sec=1)
    display.clear()
