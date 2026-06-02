# Digital Tube Module

## 1. Module Introduction

The single-digit nixie tube module is a **digital display device** composed of 7-segment light-emitting diodes, used to display 0-9 digits and simple symbols. It is widely used in counting, timing, status display, and maker DIY scenarios. It features high brightness, clear display, 3.3V/5V compatibility, simple driving, and long service life.

**Composition**:

7-segment LED light-emitting segments, common terminal, decimal point, current-limiting resistor, PCB board, wiring terminal.

**Working Principle**:

The module has a positive electrode, a negative electrode, and a segment selection signal terminal. By controlling the on/off of different segments, it combines to display 0-9 digits, and the development board controls the corresponding segments to light up by outputting levels through GPIO.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral | Development Board |
| ---------- | ----------------- |
| LED（+）   | 3.3V              |
| LED（-）   | GND               |
| LED（S）   | Optional          |

![](../../media/display1.png)

## 3.Driving Code

```python
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

```

