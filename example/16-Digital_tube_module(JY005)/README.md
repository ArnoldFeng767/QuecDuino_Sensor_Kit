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
```

