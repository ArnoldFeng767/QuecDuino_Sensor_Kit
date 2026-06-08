# Analog Piezoelectric Ceramic Vibration Module

## 1. Module Introduction

This sensor is an analog vibration sensor based on piezoelectric ceramic sheets. It utilizes the inverse transformation process where piezoelectric ceramics generate vibration from electrical signals. When the piezoelectric ceramic sheet vibrates, the signal terminal of the sensor generates an electrical signal. The module is compatible with various single-chip microcontroller control boards, such as Arduino series single-chip microcontrollers. The module includes 2 types of interfaces for your choice: one is a reverse-connection prevention white terminal with a pitch of 2.54mm. In use, we can stack a sensor expansion board on the single-chip microcontroller, connect the module with the built-in wire, and then connect it to the sensor expansion board, which is simple and convenient; the other is a pin header interface with a pitch of 2.54mm, which can be directly connected to the single-chip microcontroller using male-to-female Dupont wires.

**Working Principle**:

- **As vibration output (inverse piezoelectric effect)**: The module has power supply, ground, and signal terminals. When a pulse/square wave electrical signal is input to the signal terminal, the piezoelectric ceramic sheet deforms due to the inverse piezoelectric effect, driving the substrate to vibrate to achieve vibration feedback.
- **As vibration detection (direct piezoelectric effect)**: When the module is subjected to mechanical vibration/knocking, the piezoelectric ceramic sheet generates a weak electrical signal, which is output through the signal terminal. The development board can detect the vibration intensity through ADC acquisition.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | A1（ADC1）        |

 ![](../../media/detection1.png)



## 3.Driver Code

```python
from misc import ADC
import _thread
import utime


class VibrationSensor(object):
    """Vibration sensor class, acquires vibration intensity via ADC and
    triggers threshold alerts.

    Application scenarios: cabinet tamper detection, device drop detection,
    door/window vibration alarm, etc.
    Higher ADC values indicate stronger vibration/impact.
    """

    def __init__(self, adc_channel=None, alert_threshold=1500):
        """Initialize vibration sensor instance.

        Args:
            adc_channel: ADC channel, defaults to ADC1
            alert_threshold: Vibration alert threshold, triggers alarm when
                ADC value exceeds this value, default 1500
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.alert_threshold = alert_threshold
        self.is_running = False

    def open(self):
        """Open the ADC channel."""
        self.adc.open()

    def read_value(self):
        """Read the current vibration intensity ADC value.

        Note: Higher values generally indicate stronger vibration/impact.

        Returns:
            int: ADC sample value
        """
        return self.adc.read(self.adc_channel)

    def check_alert(self, value):
        """Check whether vibration exceeds the alert threshold.

        Application scenarios: cabinet tamper detection, device drop detection,
        door/window vibration alarm, etc.

        Args:
            value: Current ADC sample value

        Returns:
            bool: True means alert triggered
        """
        return value >= self.alert_threshold

    def monitor(self, interval_ms=200):
        """Background monitoring loop, continuously samples and outputs
        vibration state.

        Args:
            interval_ms: Sampling interval in milliseconds, default 200ms
        """
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if self.check_alert(value):
                print("Vibration alert, value = {}".format(value))
            else:
                print("Vibration value = {}".format(value))
            utime.sleep_ms(interval_ms)

    def start(self, interval_ms=200):
        """Start background monitoring thread.

        Args:
            interval_ms: Sampling interval in milliseconds, default 200ms
        """
        self.open()
        _thread.start_new_thread(self.monitor, (interval_ms,))

    def stop(self):
        """Stop background monitoring thread."""
        self.is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500)
    sensor.start()

    # Keep main thread running, wait for background monitoring
    while True:
        utime.sleep_ms(1000)
```

 