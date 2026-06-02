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
from machine import Pin
import _thread
import utime

# Sensor parameter configuration
REF_VOLTAGE = 3300       # Reference voltage (mV), 3.3V supply is 3300, 5V supply is 5000
MAX_WATER_LEVEL = 60     # Maximum water level range (mm), The height of the Water Sensor detection area is 60mm
SAMPLE_COUNT = 10        # Average filtering sampling frequency
SAMPLE_INTERVAL_MS = 5   # Sampling interval per time (ms)

def water_level_get(adc):
    """
    Get water level value (mm)
    Through multiple ADC sampling to take average filtering, then convert to actual water level depth
    Formula: water_level = (voltage / ref_voltage) * max_water_level
    """
    adc_sum = 0
    for _ in range(SAMPLE_COUNT):
        adc_sum += adc.read(adc.ADC1)
        utime.sleep_ms(SAMPLE_INTERVAL_MS)
    voltage_avg = adc_sum / SAMPLE_COUNT  # Average voltage value (mV)

    water_level = (voltage_avg / REF_VOLTAGE) * MAX_WATER_LEVEL
    return voltage_avg, round(water_level, 2)
def fun():
    while True:
        voltage, level = water_level_get(adc)
        print("Voltage: {:.1f} mV | Water Level: {:.2f} mm".format(voltage, level))
        utime.sleep(1)


if __name__ == '__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun, ())
```

 