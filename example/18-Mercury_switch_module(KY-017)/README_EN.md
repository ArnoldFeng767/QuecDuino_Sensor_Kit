# Mercury switch module

## **1. Module Introduction** 
The mercury switch module is a **gravity-sensing inclination/dumping detection digital switch device**, also known as tilt switch, angle sensor, and is commonly used in scenarios such as inclination alarm, anti-dumping protection, attitude detection, and trigger control; it relies on the flow of mercury to conduct / disconnect the circuit, output stable high or low levels, and has the advantages of **high sensitivity, reliable conduction, no mechanical contact noise, 3.3V/5V compatibility, GPIO direct reading, and small size**. 
**Luminous Principle: ** 
The module has a positive pole, a negative pole and a signal terminal. By taking advantage of the conductivity and fluidity of mercury, when tilted at a certain angle, the mercury flows and connects the electrodes, allowing the circuit to conduct; after resetting, the mercury leaves the electrodes and the circuit is disconnected. The development board determines the tilt state by reading the level.

## 2. Connection Examples 
According to the instructions provided in the table and the pictures, connect each peripheral device to the development board one by one.

| peripheral  | development board |
| ----------- | ----------------- |
| module（+） | 3.3V              |
| module（-） | GND               |
| module（S） | PIN4(GPIO31)      |

![](../../media/mercury1.png)

## 3. Driving Code

```python
from machine import Pin
import utime


class MercurySwitch(object):
    """Mercury switch sensor class, detects tilt state and controls linked output.

    Example:
        sw = MercurySwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30)
        sw.set_callback(lambda t: print("tilted!" if t else "normal"))
        sw.monitor()

    Args:
        sensor_pin:   sensor input GPIO, default GPIO31
        output_pin:   linked output GPIO, default GPIO30, pass None to disable
        trigger_level: 1=high-trigger, 0=low-trigger, default 1
        pull:          pull config, default pull-up (Pin.PULL_PU)
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU):
        self._sensor = Pin(sensor_pin, Pin.IN, pull)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._last_state = self._sensor.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """Set state change callback. callback(is_triggered)"""
        self._callback = callback

    def read_state(self):
        """Read the current level state of the sensor."""
        return self._sensor.read()

    def is_triggered(self):
        """Check whether currently in triggered state."""
        return self.read_state() == self._trigger_level

    def set_output(self, active):
        """Control linked output pin."""
        if self._output is not None:
            self._output.write(1 if active else 0)

    @property
    def trigger_count(self):
        """Get cumulative trigger count."""
        return self._trigger_count

    def reset_count(self):
        """Reset trigger count to zero."""
        self._trigger_count = 0

    def wait_for_trigger(self, timeout_ms=None):
        """Block and wait for tilt trigger."""
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
        state = self.read_state()
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
        """Polling monitor loop."""
        while True:
            changed, triggered = self._check_state()
            if changed:
                print("Mercury switch detected tilt" if triggered else "Mercury switch no tilt detected")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    sw = MercurySwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU)
    sw.monitor(interval_sec=1)
```

 