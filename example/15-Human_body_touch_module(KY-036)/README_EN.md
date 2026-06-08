# Human Touch Module

#### 1. Module Introduction

This module is a capacitive momentary touch switch module based on touch detection. The metal touch module responds to the capacitance of the human body. Since it monitors capacitance, non-metallic materials such as wood, paper, plastic and other insulating materials can be covered on the module surface to detect human touch, and it can be made into a button hidden in walls, desktops, etc.

![](../../media/finger1.png) 

**Working Principle**:

The module has a positive electrode, a negative electrode, and a signal terminal. When the human body touches the induction sheet, the capacitance value changes. After the internal circuit of the module identifies it, it outputs a high/low level signal, and the development board can directly read the state to determine whether it is touched.

#### 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/finger2.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class TouchSensor(object):
    """Human touch sensor class, detects touch state via GPIO.

    Application scenarios: touch switches, human-computer interaction,
    proximity detection, etc.
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD):
        """Initialize touch sensor instance.

        Args:
            pin: Sensor input GPIO pin number, default GPIO31
            trigger_level: Trigger level, default 1 (high level trigger)
            pull: Pull-up/down configuration, default pull-down (Pin.PULL_PD)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.trigger_level = trigger_level

    def read_state(self):
        """Read the current level state of the sensor.

        Returns:
            int: 0 or 1
        """
        return self.gpio.read()

    def is_touched(self):
        """Check whether touch is currently detected.

        Returns:
            bool: True means touch detected
        """
        return self.read_state() == self.trigger_level

    def monitor(self, interval_sec=1):
        """Polling monitor loop, detect touch state.

        Args:
            interval_sec: Polling interval in seconds, default 1 second
        """
        while True:
            if self.is_touched():
                print("Touch detected")
            else:
                print("No touch detected")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    touch_sensor = TouchSensor(pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD)
    touch_sensor.monitor(interval_sec=1)
```

