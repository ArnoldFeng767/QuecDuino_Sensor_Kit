# Key Module

## 1. Module Introduction

The key module is the **most basic digital input module**, which realizes on-off control through a tactile switch and outputs high/low level signals. It is essential for embedded/IoT projects, enabling functions such as **human-computer interaction, switch control, command triggering, counting, and mode switching**.

### 1.1 Core Parameters

- Type: Tactile key (mechanical type)
- Power supply: 3.3V – 5V
- Output: **Digital signal (high/low level)**
- Pins: 3 pins (VCC, GND, SIG)
- Default state: **High level (not pressed)**
- Trigger state: **Low level (pressed)**
- Built-in: Pull-up resistor, signal indicator light

### 1.2 Schematic Diagram

![](../../media/key1.png)

Both VCC and the resistor are integrated inside the chip. When the key is disconnected, the current flowing through the resistor is called sink current (about tens of milliamps), so the pin is at a high level at this time. When the key is pressed, it is connected to the ground and becomes a low level.

## 2. Connection Example

Connect the peripheral device to the development board one by one according to the table and image instructions.

| Peripheral   | Module       |
| ------------ | ------------ |
| **KEY（+）** | 3.3V         |
| **KEY（-）** | GND          |
| **KEY（S）** | PIN4(GPIO31) |

![](../../media/key2.png)

## 3.Driver Code

```python
import utime
from machine import ExtInt, Pin


class KeyInterrupt(object):
    """Key interrupt driver, supports interrupt detection, polling, and press counting.

    Two usage modes:
        - Interrupt mode: register a callback, auto-triggered on press
        - Polling mode:  call read_state() / is_pressed() actively

    Example:
        # Interrupt mode
        key = KeyInterrupt(Pin.GPIO31)
        key.set_callback(lambda args, cnt: print("pressed", cnt))
        key.enable()

        # Polling mode
        while True:
            if key.is_pressed():
                print("key down")
            utime.sleep_ms(100)

    Args:
        pin:         GPIO pin number, e.g. Pin.GPIO31
        mode:        interrupt trigger mode, default falling edge (ExtInt.IRQ_FALLING)
        pull:        pull-up/down config, default pull-up (Pin.PULL_PU)
        filter_time: hardware debounce time in ms, default 50
        callback:    user callback function, signature callback(args, count)
    """

    def __init__(self, pin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_PU,
                 filter_time=50, callback=None):
        self._pin_obj = Pin(pin, Pin.IN, pull)
        self._press_count = 0
        self._callback = callback
        self._extint = ExtInt(pin, mode, pull, self._irq_handler, filter_time)

    def _irq_handler(self, args):
        """Interrupt handler, runs in interrupt context — avoid blocking operations."""
        self._press_count += 1
        if self._callback:
            self._callback(args, self._press_count)

    def set_callback(self, callback):
        """Set or replace the user callback function."""
        self._callback = callback

    def enable(self):
        """Enable key interrupt."""
        self._extint.enable()

    def disable(self):
        """Disable key interrupt."""
        self._extint.disable()

    def read_state(self):
        """Read current GPIO level of the key.

        Returns:
            int: 0=pressed, 1=released
        """
        return self._pin_obj.read()

    def is_pressed(self):
        """Check if the key is currently pressed.

        Returns:
            bool: True if pressed
        """
        return self.read_state() == 0

    @property
    def count(self):
        """Get cumulative press count."""
        return self._press_count

    def reset_count(self):
        """Reset press count to zero."""
        self._press_count = 0

    def wait_for_press(self, timeout_ms=None):
        """Block and wait for key press, with optional timeout.

        Args:
            timeout_ms: timeout in ms, None for infinite wait

        Returns:
            bool: True if pressed, False on timeout
        """
        start = utime.ticks_ms()
        while True:
            if self.is_pressed():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)


def on_key_pressed(args, count):
    """Example callback, prints interrupt args and press count."""
    print("[Callback] pressed, count = {}".format(count))


if __name__ == "__main__":
    key = KeyInterrupt(
        pin=Pin.GPIO31,
        mode=ExtInt.IRQ_FALLING,
        pull=Pin.PULL_PU,
        filter_time=50,
        callback=on_key_pressed,
    )
    key.enable()
    print("Key interrupt enabled. Press the key to trigger.")

    while True:
        utime.sleep_ms(500)
```

 