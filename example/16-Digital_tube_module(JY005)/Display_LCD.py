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

    引脚映射：
        GPIO32 → a, GPIO31 → b, GPIO30 → c, GPIO33 → d,
        GPIO2  → e, GPIO3  → f, GPIO14 → g, GPIO15 → dp
    """

    # 数字 0-9 的段码表（共阳极反逻辑）
    NUM_TABLE = [
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

    def __init__(self):
        """初始化数码管显示实例，配置 8 个段码引脚为输出模式。"""
        self.segments = [
            Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 1),  # a
            Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1),  # b
            Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 1),  # c
            Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1),  # d
            Pin(Pin.GPIO2,  Pin.OUT, Pin.PULL_DISABLE, 1),  # e
            Pin(Pin.GPIO3,  Pin.OUT, Pin.PULL_DISABLE, 1),  # f
            Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1),  # g
            Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 1),  # dp
        ]

    def display_num(self, number):
        """显示指定数字（0-9）。

        Args:
            number: 要显示的数字，范围 0-9
        """
        if number < 0 or number > 9:
            return

        values = self.NUM_TABLE[number]
        for segment, value in zip(self.segments, values):
            segment.write(value)

    def clear(self):
        """清除显示（所有段熄灭）。"""
        for segment in self.segments:
            segment.write(1)

    def demo(self, interval_sec=1):
        """演示循环，依次显示 0-9。

        Args:
            interval_sec: 每个数字显示时间，单位秒，默认 1 秒
        """
        while True:
            for number in range(10):
                self.display_num(number)
                utime.sleep(interval_sec)


if __name__ == '__main__':
    display = DigitalTubeDisplay()
    display.demo(interval_sec=1)
