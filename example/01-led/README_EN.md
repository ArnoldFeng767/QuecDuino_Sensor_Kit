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
    """LED driver class, wraps GPIO pin for basic LED operations.

    Supports different hardware configurations via active_level:
        - active_level=1: high-level to light (default, source drive / common cathode)
        - active_level=0: low-level to light (sink drive / common anode)

    Example:
        led = LED(Pin.GPIO31)
        led.on()
        led.blink(times=5, interval=0.5)

    Args:
        pin:  GPIO pin number, e.g. Pin.GPIO31
        active_level: level to light the LED, 1=high-active, 0=low-active
    """

    def __init__(self, pin, active_level=1):
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)
        self.state = 0  # 0=off, 1=on (software tracked, decoupled from hardware level)

    def write(self, value):
        """Set the LED logical state.

        Args:
            value: 1=on, 0=off (logical value, independent of active_level)
        """
        self.state = value
        self.pin.write(self.active_level if value else self.inactive_level)

    def read(self):
        """Read the current LED logical state.

        Returns:
            int: 1=on, 0=off
        """
        return self.state

    def on(self):
        """Turn on the LED."""
        self.write(1)

    def off(self):
        """Turn off the LED."""
        self.write(0)

    def toggle(self):
        """Toggle the LED state (on→off, off→on)."""
        self.write(0 if self.state else 1)

    def blink(self, interval=0.5, times=None):
        """Blink the LED at the specified interval.

        Args:
            interval: duration of each on/off half-cycle in seconds, default 0.5s
            times:    number of blink cycles (on+off=1), None for infinite loop

        Example:
            led.blink(interval=0.2, times=3)   # quick flash 3 times then stop
            led.blink(interval=1.0)             # blink every second, infinite
        """
        n = 0
        while times is None or n < times:
            self.on()
            utime.sleep(interval)
            self.off()
            utime.sleep(interval)
            n += 1


if __name__ == '__main__':
    led = LED(Pin.GPIO31, active_level=1)
    # Quick flash 3 times then stay on
    led.blink(interval=0.3, times=3)
    led.on()
    print("LED test done: 3 blinks then steady on")
```

 