# Water Level Detection Module

## 1. Module Introduction

The water level monitoring module is a **resistive liquid detection sensor**, which is used in scenarios such as detecting water level height, presence or absence of water, and water leakage alarm; it detects liquid level changes through conductive probes and outputs analog signals, with advantages such as **fast response, small size, 3.3V compatibility, direct connection to ADC, and long service life**.

**Working Principle:**

The Water Sensor can monitor the water level. This module mainly utilizes the current amplification principle of transistors: when the liquid level height makes the base of the transistor conduct with the positive pole of the power supply, a certain amount of current is generated between the base and emitter of the transistor, and at this time, a current with a certain amplification factor is generated between the collector and emitter of the transistor. This current generates a characteristic voltage through the resistor at the emitter, which is collected by the AD converter.

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral | Development Board |
| ---------- | ----------------- |
| Module (+) | 3.3V              |
| Module (-) | GND               |
| Module (S) | A1（ADC1）        |

![](../../media/water1.png)

## 3.Driver Code

```python
from misc import ADC
import _thread
import utime


class WaterLevelSensor(object):
    """Water level sensor class, reads voltage via ADC and converts to water level, supports tiered alerts and callback.

    Status levels:
        STATUS_NORMAL  (0): Normal
        STATUS_WARNING (1): Warning
        STATUS_ALERT   (2): Alert

    Example:
        sensor = WaterLevelSensor(warn_level=15, alert_level=35)
        sensor.set_callback(lambda lvl, st, lbl: print(lbl))
        sensor.start()

    Args:
        adc_channel:       ADC channel, default ADC1
        ref_voltage:       reference voltage in mV, default 3300 (3.3V)
        max_water_level:   sensor max range in mm, default 60
        warn_level:        warning threshold in mm, default 15
        alert_level:       alert threshold in mm, default 35
        sample_count:      samples per reading for noise reduction, default 10
        sample_interval_ms: sampling interval in ms, default 5
    """

    STATUS_NORMAL = 0
    STATUS_WARNING = 1
    STATUS_ALERT = 2

    _STATUS_LABELS = {0: "Normal", 1: "Warning", 2: "Alert"}

    def __init__(self, adc_channel=None, ref_voltage=3300, max_water_level=60,
                 warn_level=15, alert_level=35,
                 sample_count=10, sample_interval_ms=5):
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._ref_voltage = ref_voltage
        self._max_water_level = max_water_level
        self._warn_level = warn_level
        self._alert_level = alert_level
        self._sample_count = sample_count
        self._sample_interval_ms = sample_interval_ms
        self._callback = None
        self._is_running = False

    def set_callback(self, callback):
        """Set status change callback.

        Args:
            callback: function with signature callback(level_mm, status_code, status_label)
        """
        self._callback = callback

    @property
    def warn_level(self):
        return self._warn_level

    @warn_level.setter
    def warn_level(self, value):
        self._warn_level = value

    @property
    def alert_level(self):
        return self._alert_level

    @alert_level.setter
    def alert_level(self, value):
        self._alert_level = value

    def read_voltage(self):
        """Average multiple samples to reduce ADC noise.

        Returns:
            float: averaged ADC value
        """
        adc_sum = 0
        for _ in range(self._sample_count):
            adc_sum += self._adc.read(self._adc_channel)
            utime.sleep_ms(self._sample_interval_ms)
        return adc_sum / self._sample_count

    def read_level(self):
        """Read voltage and convert to water level (single-shot, no monitor needed).

        Formula: level = (voltage / ref_voltage) * max_water_level

        Returns:
            tuple: (voltage, level_mm)
        """
        voltage_avg = self.read_voltage()
        water_level = (voltage_avg / self._ref_voltage) * self._max_water_level
        return voltage_avg, round(water_level, 2)

    def check_status(self, level):
        """Determine status code from water level.

        Args:
            level: water level in mm

        Returns:
            int: STATUS_NORMAL / STATUS_WARNING / STATUS_ALERT
        """
        if level < self._warn_level:
            return self.STATUS_NORMAL
        elif level < self._alert_level:
            return self.STATUS_WARNING
        else:
            return self.STATUS_ALERT

    @classmethod
    def status_label(cls, status_code):
        """Get label for a status code."""
        return cls._STATUS_LABELS.get(status_code, "Unknown")

    def _monitor(self, interval_sec):
        """Background monitoring loop."""
        while self._is_running:
            voltage, level = self.read_level()
            status = self.check_status(level)
            label = self.status_label(status)
            print("Level: {:.2f} mm | Voltage: {:.1f} | Status: {}".format(level, voltage, label))

            if self._callback:
                self._callback(level, status, label)

            utime.sleep(interval_sec)

    def start(self, interval_sec=1):
        """Open ADC and start background monitoring thread.

        Args:
            interval_sec: monitoring interval in seconds, default 1s
        """
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, (interval_sec,))

    def stop(self):
        """Stop background monitoring thread."""
        self._is_running = False


if __name__ == '__main__':
    def on_status(level, status, label):
        if status == WaterLevelSensor.STATUS_ALERT:
            print("!!! High water level alert !!!")

    sensor = WaterLevelSensor(
        ref_voltage=3300, max_water_level=60,
        warn_level=15, alert_level=35,
        sample_count=10, sample_interval_ms=5,
    )
    sensor.set_callback(on_status)
    sensor.start(interval_sec=1)

    while True:
        utime.sleep_ms(1000)
```

 