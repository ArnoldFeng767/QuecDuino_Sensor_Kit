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

    Example:
        ts = TouchSensor(pin=Pin.GPIO31)
        ts.set_callback(lambda t: print("touched!" if t else "released"))
        ts.monitor()

    Args:
        pin:          sensor input GPIO, default GPIO31
        trigger_level: trigger level, default 1 (high-active)
        pull:          pull config, default pull-down (Pin.PULL_PD)
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """Set touch state change callback. callback(is_touched)"""
        self._callback = callback

    def read_state(self):
        """Read the current level state of the sensor."""
        return self._gpio.read()

    def is_touched(self):
        """Check whether touch is currently detected."""
        return self.read_state() == self._trigger_level

    @property
    def trigger_count(self):
        """Get cumulative touch count."""
        return self._trigger_count

    def reset_count(self):
        """Reset touch count to zero."""
        self._trigger_count = 0

    def wait_for_touch(self, timeout_ms=None):
        """Block and wait for touch."""
        start = utime.ticks_ms()
        while True:
            if self.is_touched():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor(self, interval_sec=1):
        """Polling monitor loop."""
        while True:
            state = self.read_state()
            touched = state == self._trigger_level
            changed = touched != (self._last_state == self._trigger_level)
            self._last_state = state
            if changed:
                if touched:
                    self._trigger_count += 1
                if self._callback:
                    self._callback(touched)
                print("Touch detected" if touched else "Touch released")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    ts = TouchSensor(pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD)
    ts.monitor(interval_sec=1)
```

