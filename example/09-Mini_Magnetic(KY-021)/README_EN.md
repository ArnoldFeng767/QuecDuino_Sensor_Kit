# Mini Reed Module

## 1. Module Introduction

The mini reed, full name **Mini Reed Switch (Reed Pipe Module)**, is a passive switch component whose on-off is controlled by a magnetic field. This type of magnetic induction device is generally used for door magnetic detection, position detection, and limit triggering, and is currently widely used in embedded devices, smart hardware, and maker DIY scenarios; it can conduct when a magnetic field approaches and disconnect when the magnetic field moves away, with advantages such as small size, fast response, no mechanical contact wear, low power consumption, plug-and-play, adaptation to 3.3V/5V low-voltage environment, direct connection to GPIO detection, and long service life.

Composition of Mini Reed Module:

![](../../media/mini1.png)

**Working Principle:**

The module is essentially a switch controlled by a magnetic field. When a magnet approaches the module, the reed in the glass tube is magnetized and attracted to each other to contact, and the circuit is conducted; when the magnet moves away, the reed loses its magnetism and separates by elasticity, and the circuit is disconnected, so as to realize the switch signal output triggered by the magnetic field.

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/mini2.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class MiniMagneticController(object):
    """Mini magnetic sensor control class, magnetic field detection + output linkage.

    Example:
        ctrl = MiniMagneticController(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30)
        ctrl.set_callback(lambda t: print("triggered!" if t else "released"))
        ctrl.monitor()

    Args:
        sensor_pin:         sensor input GPIO, default GPIO31
        output_pin:         linkage output GPIO, default GPIO30, pass None to disable
        trigger_level:      trigger level, 0=low-trigger, 1=high-trigger, default 0
        output_active_level: output active level, default 1 (high-active)
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30,
                 trigger_level=0, output_active_level=1):
        self._sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PU)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._output_active = output_active_level
        self._output_inactive = 0 if output_active_level else 1
        self._last_state = self._sensor.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """Set state change callback.

        Args:
            callback: function with signature callback(is_triggered)
        """
        self._callback = callback

    def read_sensor(self):
        """Read current sensor level state."""
        return self._sensor.read()

    def is_triggered(self):
        """Check if currently in triggered state."""
        return self.read_sensor() == self._trigger_level

    def set_output(self, active):
        """Control linkage output pin level."""
        if self._output is not None:
            level = self._output_active if active else self._output_inactive
            self._output.write(level)

    @property
    def trigger_count(self):
        """Get cumulative trigger count."""
        return self._trigger_count

    def reset_count(self):
        """Reset trigger count to zero."""
        self._trigger_count = 0

    def wait_for_trigger(self, timeout_ms=None):
        """Block and wait for magnetic trigger.

        Args:
            timeout_ms: timeout in ms, None for infinite

        Returns:
            bool: True=triggered, False=timeout
        """
        start = utime.ticks_ms()
        while True:
            changed, triggered = self._check_state()
            if changed and triggered:
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def _check_state(self):
        """Detect state change, update output and count."""
        state = self.read_sensor()
        triggered = state == self._trigger_level
        self.set_output(triggered)
        changed = state != self._last_state
        if changed and triggered:
            self._trigger_count += 1
            if self._callback:
                self._callback(True)
        elif changed and not triggered:
            if self._callback:
                self._callback(False)
        self._last_state = state
        return changed, triggered

    def monitor(self, interval_sec=1):
        """Polling monitor loop, detects magnetic field and controls output.

        Args:
            interval_sec: polling interval in seconds, default 1s
        """
        while True:
            changed, triggered = self._check_state()
            if changed:
                if triggered:
                    print("[MiniMagnetic] Trigger event")
                else:
                    print("[MiniMagnetic] Release event")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    controller = MiniMagneticController(
        sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30,
        trigger_level=0, output_active_level=1,
    )
    controller.monitor()
```
