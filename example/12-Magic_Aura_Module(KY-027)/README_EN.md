# Magic Halo Module

## 1. Module Introduction

The Magic Halo Module (KY‑027) is a 2-in-1 digital module integrating **tilt sensing + LED lighting**, with a built-in mercury switch and high-brightness LED. It is used for tilt detection, posture triggering, status indication, and maker interaction projects. The module features small size, fast response, digital level output, 3.3V/5V compatibility, direct GPIO driving, and stable service life.

**Working Principle**:

![](../../media/magic1.png)

The module has power supply, ground, signal output, and LED control terminals. When tilted to a certain angle, the mercury switch is turned on/off to output high/low level; the LED can be controlled to turn on/off via GPIO to achieve effects such as tilt lighting and posture alarm.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |
| Module（L） | PIN5(GPIO30)      |

![](../../media/magic2.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class TiltSwitch(object):
    """Tilt switch sensor class, detects device posture and controls output linkage.

    Example:
        ts = TiltSwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30)
        ts.set_callback(lambda t: print("tilted!" if t else "normal"))
        ts.monitor()

    Args:
        sensor_pin:   sensor input GPIO, default GPIO31
        output_pin:   linkage output GPIO, default GPIO30, pass None to disable
        trigger_level: 1=high-trigger, 0=low-trigger, default 1
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        self._sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._last_state = self._sensor.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """Set state change callback. callback(is_tilted)"""
        self._callback = callback

    def read_state(self):
        """Read current sensor level state."""
        return self._sensor.read()

    def is_tilted(self):
        """Check if currently in tilted state."""
        return self.read_state() == self._trigger_level

    def set_output(self, active):
        """Control linkage output pin."""
        if self._output is not None:
            self._output.write(1 if active else 0)

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

    def _check_state(self):
        state = self.read_state()
        tilted = state == self._trigger_level
        self.set_output(tilted)
        changed = state != self._last_state
        if changed and tilted:
            self._trigger_count += 1
            if self._callback:
                self._callback(True)
        elif changed and not tilted:
            if self._callback:
                self._callback(False)
        self._last_state = state
        return changed, tilted

    def monitor(self, interval_sec=1):
        """Polling monitor loop."""
        while True:
            changed, tilted = self._check_state()
            if changed:
                print("Tilt detected" if tilted else "Normal position")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    ts = TiltSwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    ts.monitor(interval_sec=1)
```
