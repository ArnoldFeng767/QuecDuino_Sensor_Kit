# Laser Emission Module

## 1. Module Introduction

The core principle of the **Laser Emitter Module** is: **converting electrical energy into high-brightness, high-directionality, monochromatic coherent light (laser) efficiently through a semiconductor laser diode (LD), then emitting it after collimation/shaping by an optical system**. It is widely used in laser ranging, laser radar, optical fiber communication, laser indication, infrared night vision and other scenarios.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/laser1.png)

## 3. Driver Code

```python
from machine import Pin
import utime

class LaserEmitter:
    """Laser emission module packaging class."""

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        self.gpio.write(self.active_level)
        print("laser on")

    def off(self):
        self.gpio.write(self.inactive_level)
        print("laser off")

    def blink(self,):
        self.on()
        utime.sleep(2)
        self.off()
        utime.sleep(2)

    def demo(self):
        while True:
            self.blink()


if __name__ == '__main__':
    laser = LaserEmitter(pin=Pin.GPIO31, active_level=1)
    laser.demo()
        
```

