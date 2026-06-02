"""
@file      : pressure_detection.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based vibration/impact detection using ADC
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
import _thread
import utime


class VibrationSensor:
    """Vibration sensor encapsulation class."""

    def __init__(self, adc_channel=None, alert_threshold=1500):
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.alert_threshold = alert_threshold
        self.is_running = False

    def open(self):
        self.adc.open()

    def read_value(self):
        # The larger the value, the stronger the impact/vibration is usually indicated.
        return self.adc.read(self.adc_channel)

    def check_alert(self, value):
        # Actual application: cabinet tamper detection, device drop detection, door/window vibration alarm.
        return value >= self.alert_threshold

    def monitor(self):
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if self.check_alert(value):
                print("Vibration alert, value = {}".format(value))
            else:
                print("Vibration value = {}".format(value))
            utime.sleep_ms(200)

    def start(self):
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500)
    sensor.start()

    while True:
        utime.sleep_ms(1000)