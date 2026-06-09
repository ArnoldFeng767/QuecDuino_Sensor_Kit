# KY-025 Reed Switch Sensor Module Introduction

The KY-025 is a magnetic control sensor module based on the principle of **Reed Switch (also known as Reed Pipe)**. It is essentially a miniature electrical switch controlled by a magnetic field. When a magnet approaches, the internal metal reed will close to conduct the circuit; when the magnet moves away, the reed will automatically bounce open to disconnect the circuit.

Due to its simple structure, high sensitivity and trigger without direct contact, the KY-025 is often used as a non-contact proximity detection or position limit device in various IoT projects.

![](../../media/reed1.png)

### Core Features

- **Dual signal output**: The module provides both digital (DO) and analog (AO) output interfaces, which can not only make simple switch judgments, but also perceive the relative change of magnetic field intensity.
- **Adjustable sensitivity**: The onboard precision potentiometer (trim knob) can rotate to adjust the detection distance and trigger sensitivity of the sensor according to the actual application scenario.
- **Intuitive working indication**: Equipped with power indicator light and working status LED. When the magnetic field trigger is detected, the onboard LED will light up, which is convenient for debugging and observation.
- **Wide voltage compatibility**: It usually supports wide voltage power supply from 3.3V to 5V, and can perfectly adapt to various mainstream single-chip microcomputer development boards such as Arduino, STM32 and QuecDuino in your hand.

### Pin Description and Wiring

The KY-025 module usually leads out 4 standard pins, and the specific definitions are as follows:

| Pin Name    | Function Description  | Wiring Suggestion                                            |
| :---------- | :-------------------- | :----------------------------------------------------------- |
| **+ (VCC)** | Positive power supply | Connect to 3.3V or 5V of the development board               |
| **G (GND)** | Negative power supply | Connect to GND of the development board                      |
| **D0**      | Digital signal output | Connect to ordinary GPIO of the development board (such as pin 4) |
| **A0**      | Analog signal output  | Connect to ADC pin of the development board (such as A0)     |

### Detailed Working Principle

1. **Digital Output (D0)**: This is a switch signal. After adjusting the sensitivity, once a magnet enters the effective detection range, pin 4 will output a high level (or low level, depending on the specific circuit design), and the onboard LED will light up at the same time; it will return to the original state after the magnet is removed. This is very suitable for making "door magnetic alarm" or "in-position detection".
2. **Analog Output (A0)**: The voltage value output by this pin will change linearly with the change of magnetic field intensity. Usually, a higher value is output when there is no magnetic field, and the output voltage will gradually decrease as the magnet approaches. By reading this analog value, you can roughly judge the distance between the magnet and the sensor.

### Common Application Scenarios

- **Door and window anti-theft alarm**: Install the module on the door frame and the magnet on the door leaf, and the alarm will be triggered when the door is opened.
- **Intelligent counting and speed measurement**: Install a magnet on the fan blade or rotating object, which is triggered once per revolution, so as to calculate the speed or accumulate the number of times.
- **Position limit detection**: Used on robotic arms or mobile trolleys to detect whether the preset physical boundary is reached.
- **Contactless switch**: As a trigger for opening the cover to turn on the light of jewelry boxes and gift boxes, it is both hidden and durable.

### Driver Code

#### ADC Mode (Analog magnetic field intensity)

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class MagneticReedSwitch(object):
    """Magnetic reed switch sensor class (ADC mode), reads magnetic field intensity via analog signal.

    Application scenarios: door/window anti-theft, smart counting, position limit detection, contactless switch, etc.
    When ADC value exceeds threshold, magnetic field is detected and LED lights up.
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, threshold=100):
        """Initialize magnetic reed switch sensor instance (ADC mode).

        Args:
            adc_channel: ADC channel, defaults to ADC1
            led_pin: LED indicator GPIO pin number, defaults to GPIO31
            threshold: Magnetic field intensity threshold, defaults to 100
        """
        self.threshold = threshold
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def open(self):
        """Open ADC channel."""
        self.adc.open()

    def read_value(self):
        """Read current magnetic field ADC value."""
        return self.adc.read(self.adc_channel)

    def handle_magnetic_field(self, value):
        """Control LED based on magnetic field intensity."""
        if value > self.threshold:
            self.led.write(1)
        else:
            self.led.write(0)

    def monitor(self):
        """Background monitoring loop, continuously samples and outputs magnetic field status."""
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            status = "Magnetic field detected" if value > self.threshold else "No magnetic field"
            print("ADC: {} | Status: {}".format(value, status))
            self.handle_magnetic_field(value)
            utime.sleep_ms(500)

    def start(self):
        """Start background sampling thread."""
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        """Stop background sampling thread."""
        self.is_running = False


if __name__ == '__main__':
    magnetic_reed_switch = MagneticReedSwitch(
        led_pin=Pin.GPIO31,
        threshold=100,
    )
    magnetic_reed_switch.start()

    # Keep main thread alive
    while True:
        utime.sleep_ms(1000)
```

#### GPIO Mode (Digital switch state detection)

```python
from machine import Pin
import utime


class ReedSwitch(object):
    """Reed switch sensor class (GPIO mode), detects magnetic field state changes via digital signal.

    Application scenarios: door/window anti-theft alarm, liquid level float switch, equipment in-place detection, etc.
    Common wiring is pull-up input, output low when magnet approaches (triggered).
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        """Initialize reed switch sensor instance (GPIO mode).

        Args:
            pin: GPIO pin number, defaults to GPIO31
            trigger_level: Trigger level, 0 = low level trigger, 1 = high level trigger, defaults to 0
            pull: Pull-up/down config, defaults to pull-up (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.trigger_level = trigger_level
        self.last_state = self.gpio.read()

    def read_state(self):
        """Read current GPIO level state."""
        return self.gpio.read()

    def is_triggered(self):
        """Check if currently in triggered state."""
        return self.read_state() == self.trigger_level

    def check_state_change(self):
        """Detect whether state has changed.

        Application scenario: door magnetic alarm — door open triggers alarm, door close returns to normal.
        """
        current = self.read_state()
        changed = current != self.last_state
        self.last_state = current
        return changed, current

    def monitor(self, interval_sec=1):
        """Polling monitor loop, detects and outputs magnetic field state changes."""
        while True:
            changed, state = self.check_state_change()

            if changed:
                if state == self.trigger_level:
                    print("[ReedSwitch] Triggered: magnetic field change detected")
                else:
                    print("[ReedSwitch] Released: magnetic field back to normal")
            else:
                print("[ReedSwitch] Stable: no state change")

            utime.sleep(interval_sec)


if __name__ == "__main__":
    # Default pull-up input, low level trigger
    sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    sensor.monitor(interval_sec=1)
```

