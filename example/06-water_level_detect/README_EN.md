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
    """Water level sensor class, reads voltage via ADC and converts to water level, supports tiered alerts.

    Application scenarios: tank level monitoring, leak detection, flood warning, etc.
    Three-tier status indication via warn_level and alert_level thresholds.

    Status levels:
        - Normal: level < warn_level
        - Warning: warn_level <= level < alert_level
        - Alert: level >= alert_level
    """

    def __init__(self, adc_channel=None, ref_voltage=3300, max_water_level=60,
                 warn_level=15, alert_level=35,
                 sample_count=10, sample_interval_ms=5):
        """Initialize water level sensor instance.

        Args:
            adc_channel: ADC channel, defaults to ADC1
            ref_voltage: Reference voltage in mV, defaults to 3300mV (3.3V)
            max_water_level: Sensor max range in mm, defaults to 60mm
            warn_level: Warning threshold in mm, defaults to 15mm
            alert_level: Alert threshold in mm, defaults to 35mm
            sample_count: Number of samples per reading for noise reduction, defaults to 10
            sample_interval_ms: Sampling interval in ms, defaults to 5ms
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.ref_voltage = ref_voltage
        self.max_water_level = max_water_level
        self.warn_level = warn_level
        self.alert_level = alert_level
        self.sample_count = sample_count
        self.sample_interval_ms = sample_interval_ms
        self.is_running = False

    def open(self):
        """Open ADC channel."""
        self.adc.open()

    def read_voltage(self):
        """Average multiple samples to reduce ADC noise."""
        adc_sum = 0
        for _ in range(self.sample_count):
            adc_sum += self.adc.read(self.adc_channel)
            utime.sleep_ms(self.sample_interval_ms)
        return adc_sum / self.sample_count

    def read_level(self):
        """Read voltage and convert to water level.

        Formula: level = (voltage / ref_voltage) * max_water_level
        Note: Assumes linear voltage-level relationship. Calibrate with actual sensor curve in production.
        """
        voltage_avg = self.read_voltage()
        water_level = (voltage_avg / self.ref_voltage) * self.max_water_level
        return voltage_avg, round(water_level, 2)

    def check_status(self, level):
        """Determine status based on water level.

        Application scenarios: tank level monitoring, leak alarm, flood warning, etc.

        Args:
            level: Water level in mm

        Returns:
            str: Status description ("Normal" / "Warning" / "Alert")
        """
        if level < self.warn_level:
            return "Normal"
        elif level < self.alert_level:
            return "Warning"
        else:
            return "Alert"

    def monitor(self, interval_sec=1):
        """Background monitoring loop, continuously samples and outputs level with status."""
        self.is_running = True
        while self.is_running:
            voltage, level = self.read_level()
            status = self.check_status(level)
            print("Level: {:.2f} mm | Voltage: {:.1f} | Status: {}".format(level, voltage, status))
            utime.sleep(interval_sec)

    def start(self, interval_sec=1):
        """Start background monitoring thread."""
        self.open()
        _thread.start_new_thread(self.monitor, (interval_sec,))

    def stop(self):
        """Stop background monitoring thread."""
        self.is_running = False


if __name__ == '__main__':
    water_sensor = WaterLevelSensor(
        ref_voltage=3300,
        max_water_level=60,
        warn_level=15,
        alert_level=35,
        sample_count=10,
        sample_interval_ms=5,
    )
    water_sensor.start(interval_sec=1)

    # Keep main thread alive
    while True:
        utime.sleep_ms(1000)
```

 