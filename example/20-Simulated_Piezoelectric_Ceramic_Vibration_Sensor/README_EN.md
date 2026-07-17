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
    """Vibration sensor class, acquires vibration intensity via ADC with threshold alerts.

    Example:
        sensor = VibrationSensor(alert_threshold=1500)
        sensor.set_callback(lambda val: print("vibration!", val))
        sensor.start()

    Args:
        adc_channel:    ADC channel, default ADC1
        alert_threshold: alert threshold, default 1500
        sample_ms:      sampling interval in ms, default 200
    """

    def __init__(self, adc_channel=None, alert_threshold=1500, sample_ms=200):
        self._alert_threshold = alert_threshold
        self._sample_ms = sample_ms
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0

    def set_callback(self, callback):
        """Set vibration alert callback. callback(adc_value)"""
        self._callback = callback

    @property
    def alert_threshold(self):
        return self._alert_threshold

    @alert_threshold.setter
    def alert_threshold(self, value):
        self._alert_threshold = value

    def read_value(self):
        """Read the current vibration intensity ADC value."""
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_alert(self, value=None):
        """Check whether vibration exceeds alert threshold."""
        v = value if value is not None else self._last_value
        return v >= self._alert_threshold

    def _monitor(self):
        """Background monitoring loop."""
        while self._is_running:
            value = self.read_value()
            if value >= self._alert_threshold:
                print("Vibration alert, value = {}".format(value))
                if self._callback:
                    self._callback(value)
            utime.sleep_ms(self._sample_ms)

    def start(self):
        """Open ADC and start background monitoring thread."""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """Stop background monitoring thread."""
        self._is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500, sample_ms=200)
    sensor.set_callback(lambda v: print("Alert triggered! ADC={}".format(v)))
    sensor.start()

    while True:
        utime.sleep_ms(1000)
```

 