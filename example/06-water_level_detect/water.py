
"""
@file      : water.py
@author    : Aaron Chen
@brief     : Water level sensor demo using ADC with water level conversion
@version   : 0.2
@date      : 2026-04-10
@copyright : Copyright (c) 2026
"""

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