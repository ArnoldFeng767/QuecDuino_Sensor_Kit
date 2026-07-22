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
    """Tilt switch sensor class, detects tilt state via GPIO and controls LED.

    Example:
        sw = InclinationSwitch(pin=Pin.GPIO31, led_pin=Pin.GPIO32)
        sw.set_callback(lambda t: print("tilted!" if t else "level"))
        sw.monitor()

    Args:
        pin:          sensor input GPIO, default GPIO31
        led_pin:      LED indicator GPIO, default GPIO32, pass None to disable
        trigger_level: 0=low-trigger, 1=high-trigger, default 0
        pull:          pull config, default pull-up (Pin.PULL_PU)
    """

    def __init__(self, pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """Set state change callback. callback(is_tilted)"""
        self._callback = callback

    def read_state(self):
        """Read current sensor level state."""
        return self._gpio.read()

    def is_tilted(self):
        """Check if currently in tilted state."""
        return self.read_state() == self._trigger_level

    def _update_led(self, tilted):
        if self._led is not None:
            self._led.write(1 if tilted else 0)

    @property
    def trigger_count(self):
        """Get cumulative trigger count."""
        return self._trigger_count

    def reset_count(self):
        """Reset trigger count to zero."""
        self._trigger_count = 0

    def wait_for_tilt(self, timeout_ms=None):
        """Block and wait for tilt trigger."""
        start = utime.ticks_ms()
        while True:
            if self.is_tilted():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor(self, interval_sec=1):
        """Polling monitor loop."""
        while True:
            tilted = self.is_tilted()
            self._update_led(tilted)
            changed = tilted != (self._last_state == self._trigger_level)
            self._last_state = 1 if tilted else 0
            if changed:
                if tilted:
                    self._trigger_count += 1
                if self._callback:
                    self._callback(tilted)
                print("Tilt detected" if tilted else "Level state")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    sw = InclinationSwitch(pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU)
    sw.monitor(interval_sec=1)
```
