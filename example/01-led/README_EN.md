# LED module

## **1. Module Introduction**

LED Principles and Industry Classification: LED is the abbreviation for Light Emitting Diode (Light Emitting Diode, LED), also known as light-emitting diode. Since its development, this semiconductor component has generally been used as indicator lights and display panels. However, with the advancement of technology, it can now be used as a light source. It not only can directly convert electrical energy into light energy with high efficiency, but also has a lifespan of up to tens of thousands to 100,000 hours. At the same time, it is less fragile than traditional bulbs, can save electricity, is environmentally friendly without mercury, has a small size, can be applied in low-temperature environments, has directional light, causes less light pollution, and has a rich color gamut.

**LED Composition:**

![](../../media/led1.png)

**Luminous Principle:**

![](../../media/led2.png)

On the left is the positive pole, and on the right is the negative pole. When a voltage difference is formed between the positive and negative poles, the LED lights up.

## 2. Connection Examples

According to the instructions provided in the table and pictures, connect the peripherals one by one to the development board.

| peripheral | development board |
| ---------- | ----------------- |
| LED（+）   | 3.3V              |
| LED（-）   | GND               |
| LED（S）   | PIN4(GPIO31)      |

 

![](../../media/led3.png)

## 3. Driving Code

```python
from machine import Pin
import utime


class LED(object):
    """LED control class, wraps GPIO pin for basic LED operations.

    Args:
        pin: GPIO pin number, e.g. Pin.GPIO31
    """

    def __init__(self, pin):
        # Initialize GPIO as output mode, disable pull-up/down resistor, default low (LED off)
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)

    def write(self, value):
        """Set the LED pin level.

        Args:
            value: 1 for high (on), 0 for low (off)
        """
        self.pin.write(value)

    def read(self):
        """Read the current LED pin level.

        Returns:
            int: 1 or 0
        """
        return self.pin.read()

    def on(self):
        """Turn on the LED (output high)."""
        self.pin.write(1)

    def off(self):
        """Turn off the LED (output low)."""
        self.pin.write(0)

    def blink(self, interval=1):
        """Blink the LED at the specified interval.

        Args:
            interval: on/off toggle interval in seconds, default 1
        """
        while True:
            self.on()
            utime.sleep(interval)
            self.off()
            utime.sleep(interval)


if __name__ == '__main__':
    # Create LED instance on GPIO31
    led = LED(Pin.GPIO31)
    # Run blink test (toggle every 1 second)
    led.blink()
```

 