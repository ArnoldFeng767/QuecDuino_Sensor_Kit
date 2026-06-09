# LED Module

## 1. Module Introduction

The tricolor RGBLED is a **full-color light-emitting diode module**, which consists of three chips (red, green, and blue) packaged together. It can mix any color by adjusting brightness through PWM (Pulse Width Modulation), and is widely used in ambient lights, status indicators, interactive prompts, maker DIY scenarios. It can achieve effects such as seven-color gradient, breathing, and flashing, with advantages including small size, high brightness, 3.3V/5V compatibility, simple driving, and long service life.

**Light-emitting Principle**:

The LED pins share a common ground. The LED lights up when a voltage difference is formed between the positive and negative poles, so a high level turns on the LED.

## 2. Connection Example

Connect the peripheral to the development board one by one according to the guidance of the table and picture.

| Peripheral | Development Board |
| ---------- | ----------------- |
| LED（-）   | GND               |
| LED（R）   | PIN4（GPIO31）    |
| LED（G）   | PIN5（GPIO30）    |
| LED（B）   | PIN6（GPIO32）    |

![](../../media/led4.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class RGBLED(object):
    """RGB LED control class, mixes colors via three GPIO pins (R, G, B).

    Note: Common-anode wiring — inverted logic: 0 = on, 1 = off.
    """

    def __init__(self, red_pin, green_pin, blue_pin):
        """Initialize RGB LED instance.

        Args:
            red_pin: Red channel GPIO pin (Pin object)
            green_pin: Green channel GPIO pin (Pin object)
            blue_pin: Blue channel GPIO pin (Pin object)
        """
        self.red = red_pin
        self.green = green_pin
        self.blue = blue_pin

    def set_color(self, r, g, b):
        """Set RGB channel levels directly.

        Note: Common-anode inverted logic, 0 = on, 1 = off.

        Args:
            r: Red channel level (0 or 1)
            g: Green channel level (0 or 1)
            b: Blue channel level (0 or 1)
        """
        self.red.write(r)
        self.green.write(g)
        self.blue.write(b)

    def set_color_by_name(self, name):
        """Set LED color by name.

        Supported colors: red, green, blue, yellow, purple, cyan, white, off
        """
        # Common-anode inverted logic: 0 = on, 1 = off
        color_map = {
            "red":    (0, 1, 1),  # Red only
            "green":  (1, 0, 1),  # Green only
            "blue":   (1, 1, 0),  # Blue only
            "yellow": (0, 0, 1),  # Red + Green
            "purple": (0, 1, 0),  # Red + Blue
            "cyan":   (1, 0, 0),  # Green + Blue
            "white":  (0, 0, 0),  # Red + Green + Blue (all on)
            "off":    (1, 1, 1),  # All off
        }
        if name in color_map:
            self.set_color(*color_map[name])


if __name__ == "__main__":
    # Pin mapping: R -> GPIO32, G -> GPIO30, B -> GPIO31
    rgb_led = RGBLED(
        red_pin=Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0),
        green_pin=Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0),
        blue_pin=Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 0),
    )

    # Cycle through all preset colors
    colors = ["red", "green", "blue", "yellow", "purple", "cyan", "white", "off"]
    while True:
        for color in colors:
            rgb_led.set_color_by_name(color)
            print("LED color set to {}".format(color))
            utime.sleep(1)
```

