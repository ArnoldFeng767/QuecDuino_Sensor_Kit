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

    def __init__(self, pin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_PU, filter_time=50, user_callback=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        self.filter_time = filter_time
        self.user_callback = user_callback
        self.press_count = 0
        # Register external interrupt, triggered on key press
        self._extint = ExtInt(self.pin, self.mode, self.pull, self._irq_handler, self.filter_time)

    def _irq_handler(self, args):
        self.press_count += 1
        print("[KeyInterrupt] key pressed, count = {}".format(self.press_count))
        if self.user_callback:
            self.user_callback(args, self.press_count)

    def enable(self):
        self._extint.enable()

    def disable(self):
        self._extint.disable()

    def reset_count(self):
        self.press_count = 0


def on_key_pressed(args, count):
    print("[UserCallback] args = {}, count = {}".format(args, count))


if __name__ == "__main__":
    # Modify according to the actual pins of your development board, e.g. Pin.GPIO31
    key = KeyInterrupt(
        pin=Pin.GPIO31,
        mode=ExtInt.IRQ_FALLING,
        pull=Pin.PULL_PU,
        filter_time=50,
        user_callback=on_key_pressed,
    )
    key.enable()

    print("Key interrupt is enabled. Press the key to trigger interrupt.")
    # Keep main thread alive, waiting for interrupt
    while True:
        utime.sleep_ms(500)
```

 