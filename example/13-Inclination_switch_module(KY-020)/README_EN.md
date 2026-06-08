# Tilt Switch Module

## 1. Module Introduction

The tilt switch is a **posture-sensing digital switch device**, also known as a ball switch or topple sensor. It is commonly used in tilt detection, anti-toppling protection, posture triggering, and intelligent alarm scenarios. It can automatically switch level signals when the module is tilted to a certain angle. It has the advantages of small size, no contacts, low power consumption, 3.3V/5V compatibility, direct GPIO detection, sensitive response, and long service life.

**Working Principle**:

The module has a positive electrode, a negative electrode, and a signal terminal. When tilted, the internal ball/conductive liquid moves, turning the internal contacts on or off to output high/low levels. The development board can directly read the state to determine whether it is tilted.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/lnclination1.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class InclinationSwitch(object):
    """Tilt switch sensor class, detects tilt state via GPIO and controls LED indicator.

    Application scenarios: tipping alarm, equipment posture detection, transportation vibration indication, etc.
    """

    def __init__(self, pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU):
        """Initialize tilt switch sensor instance.

        Args:
            pin: Sensor input GPIO pin number, defaults to GPIO31
            led_pin: LED indicator GPIO pin number, defaults to GPIO32
            trigger_level: Trigger level, defaults to 0 (low level trigger)
            pull: Pull-up/down config, defaults to pull-up (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        """Read current sensor level state."""
        return self.gpio.read()

    def is_tilted(self):
        """Check if currently in tilted state."""
        return self.read_state() == self.trigger_level

    def monitor(self, interval_sec=1):
        """Polling monitor loop, detects tilt state and controls LED."""
        while True:
            if self.is_tilted():
                self.led.write(1)
                print("Tilt detected")
            else:
                self.led.write(0)
                print("Level state")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    tilt_switch = InclinationSwitch(pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU)
    tilt_switch.monitor(interval_sec=1)
```
