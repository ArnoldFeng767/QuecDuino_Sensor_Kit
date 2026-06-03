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

class WaterLevelSensor:
    """Water level sensor packaging type"""

    def __init__(self, adc_channel=None, ref_voltage=3300, max_water_level=60, sample_count=10, sample_interval_ms=5):
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.ref_voltage = ref_voltage
        self.max_water_level = max_water_level
        self.sample_count = sample_count
        self.sample_interval_ms = sample_interval_ms
        self.is_running = False

    def open(self):
        self.adc.open()
    def read_voltage(self):
        adc_sum = 0
        for _ in range(self.sample_count):
            adc_sum += self.adc.read(self.adc_channel)
            utime.sleep_ms(self.sample_interval_ms)
        return adc_sum / self.sample_count

    def read_level(self):
        voltage_avg = self.read_voltage()
        water_level = (voltage_avg / self.ref_voltage) * self.max_water_level
        return voltage_avg, round(water_level, 2)

    def monitor(self, interval_sec=1):
        self.is_running = True
        while self.is_running:
            voltage, level = self.read_level()
            print("Voltage: {:.1f} mV | Water Level: {:.2f} mm".format(voltage, level))
            utime.sleep(interval_sec)

    def start(self, interval_sec=1):
        self.open()
        _thread.start_new_thread(self.monitor, (interval_sec,))

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    water_sensor = WaterLevelSensor(
        ref_voltage=3300,
        max_water_level=60,
        sample_count=10,
        sample_interval_ms=5,
    )
    water_sensor.start(interval_sec=1)

    while True:
        utime.sleep_ms(1000)
```

 