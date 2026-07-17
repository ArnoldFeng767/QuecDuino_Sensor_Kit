# 数码管模块

## **一、** **模块介绍**

单位数码管模块是**数字显示器件**，由 7 段发光二极管组成，用于显示 0-9 数字及简单符号，广泛用于计数、计时、状态显示、创客 DIY 场景；它亮度高、显示清晰、3.3V/5V 兼容、驱动简单、使用寿命长。

**LED组成：**

7 段 LED 发光段、公共端、小数点、限流电阻、PCB 板、接线端子

**发光原理：**

模块有正极、负极、段选信号端。通过控制不同段的亮灭，组合显示 0-9 数字，开发板通过 GPIO 输出电平控制对应段点亮。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设     | 开发板 |
| -------- | ------ |
| LED（+） | 3.3V   |
| LED（-） | GND    |
| LED（S） | 自选   |

![](../../media/display1.png)

## 三、 驱动代码

```python
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
        display.clear()

    Args:
        auto_clear: 每次显示前自动清除，默认 True
    """

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

    def show(self, number):
        """显示指定数字（0-9），超出范围自动忽略。"""
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

    def countdown(self, start=9, end=0, interval_sec=1):
        """倒计时显示。"""
        step = -1 if start > end else 1
        for n in range(start, end + step, step):
            self.show(n)
            utime.sleep(interval_sec)

    def demo(self, interval_sec=1):
        """演示循环，依次显示 0-9。"""
        while True:
            for n in range(10):
                self.show(n)
                utime.sleep(interval_sec)


if __name__ == '__main__':
    display = DigitalTubeDisplay()
    display.countdown(9, 0, interval_sec=1)
    display.clear()
```

