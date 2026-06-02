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

class DigitalTubeDisplay:
    """单个 8 段数码管显示类。"""

    NUM_TABLE = [
        [0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 0],
    ]

    def __init__(self):
        self.segments = [
            Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO2, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO3, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1),
            Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 1),
        ]

    def display_num(self, number):
        if number < 0 or number > 9:
            return

        values = self.NUM_TABLE[number]
        for segment, value in zip(self.segments, values):
            segment.write(value)

    def clear(self):
        for segment in self.segments:
            segment.write(1)

    def demo(self, interval_sec=1):
        while True:
            for number in range(10):
                self.display_num(number)
                utime.sleep(interval_sec)


if __name__ == '__main__':
    display = DigitalTubeDisplay()
    display.demo(interval_sec=1)
