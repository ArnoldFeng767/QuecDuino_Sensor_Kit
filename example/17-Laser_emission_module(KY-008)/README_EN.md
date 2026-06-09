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


class LaserEmitter(object):
    """Laser emitter control class, controls laser on/off and blinking via GPIO.

    Adapts to different trigger modes via the active_level parameter.
    Application scenarios: laser indication, alignment assistance,
    security warning, etc.
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        """Initialize laser emitter instance.

        Args:
            pin: GPIO pin number, default GPIO31
            active_level: Trigger level, 1 = high level trigger,
                0 = low level trigger, default 1
        """
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        """Turn on the laser."""
        self.gpio.write(self.active_level)
        print("Laser on")

    def off(self):
        """Turn off the laser."""
        self.gpio.write(self.inactive_level)
        print("Laser off")

    def blink(self, interval=2):
        """Blink the laser once (on -> off).

        Args:
            interval: On/off interval in seconds, default 2 seconds
        """
        self.on()
        utime.sleep(interval)
        self.off()
        utime.sleep(interval)

    def demo(self, interval=2):
        """Demo loop, continuous blinking.

        Args:
            interval: Blink interval in seconds, default 2 seconds
        """
        while True:
            self.blink(interval)


if __name__ == '__main__':
    laser = LaserEmitter(pin=Pin.GPIO31, active_level=1)
    laser.demo(interval=2)
```

