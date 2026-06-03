"""
@file      : Buzzer.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Active and passive buzzer driver classes
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class ActiveBuzzer:
    """Active buzzer driver type."""

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        self.gpio.write(self.active_level)

    def off(self):
        self.gpio.write(self.inactive_level)

    def beep(self, duration_ms=200):
        self.on()
        utime.sleep_ms(duration_ms)
        self.off()

    def beep_times(self, times=3, duration_ms=200, interval_ms=200):
        for _ in range(times):
            self.beep(duration_ms)
            utime.sleep_ms(interval_ms)



if __name__ == '__main__':
    active_buzzer = ActiveBuzzer(pin=Pin.GPIO31, active_level=1)
    active_buzzer.beep_times(times=15, duration_ms=300, interval_ms=300)
    utime.sleep_ms(1000)
 