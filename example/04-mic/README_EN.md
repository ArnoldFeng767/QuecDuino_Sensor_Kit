# Microphone Module

## 1. Module Introduction

A microphone is short for an **acoustic-electric conversion device**, also known as a sound detection sensor module. It can detect the sound intensity in the surrounding environment and convert it into an electrical signal for output. It contains a built-in microphone that can capture sound signals. The sensitivity of the module to sound can be adjusted by tuning the sensitivity potentiometer on the module. It supports analog output mode, meeting the requirements of most applications and design needs.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the guidance of the table and picture.

| Peripheral | Development Board |
| ---------- | ----------------- |
| MIC（+）   | 3.3V              |
| MIC（-）   | GND               |
| MIC（S）   | A1(ADC1)          |

![](../../media/mic1.png) 



## 3.Driver Code

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class Mic(object):
    """Microphone sensor class, reads sound intensity via ADC with threshold trigger and callback.

    Example:
        mic = Mic(led_pin=Pin.GPIO31, threshold=200)
        mic.set_callback(lambda val: print("loud!", val))
        mic.start()

    Args:
        adc_channel: ADC channel, default ADC1
        led_pin:     LED indicator GPIO pin, default GPIO31, pass None to disable
        threshold:   sound intensity threshold, default 200
        sample_ms:   sampling interval in ms, default 500
        led_on_ms:   LED on duration in ms, default 500 (non-blocking)
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 threshold=200, sample_ms=500, led_on_ms=500):
        self._threshold = threshold
        self._sample_ms = sample_ms
        self._led_on_ms = led_on_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0
        self._led_off_at = 0

    def set_callback(self, callback):
        """Set sound trigger callback.

        Args:
            callback: callback function, signature callback(value), pass None to clear
        """
        self._callback = callback

    @property
    def threshold(self):
        """Current trigger threshold."""
        return self._threshold

    @threshold.setter
    def threshold(self, value):
        """Change threshold at runtime."""
        self._threshold = value

    def read_value(self):
        """Read current sound intensity ADC value.

        Returns:
            int: ADC reading
        """
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_detected(self):
        """Check if last sample exceeded threshold.

        Returns:
            bool: True if sound detected
        """
        return self._last_value > self._threshold

    def _led_on(self):
        """Turn LED on (non-blocking)."""
        if self._led is not None:
            self._led.write(1)
            self._led_off_at = utime.ticks_ms() + self._led_on_ms

    def _led_tick(self):
        """Check if LED should be turned off."""
        if self._led is not None and self._led_off_at > 0:
            if utime.ticks_diff(utime.ticks_ms(), self._led_off_at) >= 0:
                self._led.write(0)
                self._led_off_at = 0

    def _monitor(self):
        """Background monitoring loop, non-blocking sampling with callback and LED."""
        while self._is_running:
            value = self.read_value()

            if value > self._threshold:
                self._led_on()
                if self._callback:
                    self._callback(value)

            self._led_tick()
            utime.sleep_ms(self._sample_ms)

    def start(self):
        """Open ADC and start background monitoring thread."""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """Stop monitoring thread and turn off LED."""
        self._is_running = False
        if self._led is not None:
            self._led.write(0)


if __name__ == '__main__':
    def on_sound(value):
        print("Sound detected! ADC = {}".format(value))

    mic = Mic(led_pin=Pin.GPIO31, threshold=200, sample_ms=500, led_on_ms=500)
    mic.set_callback(on_sound)
    mic.start()

    while True:
        utime.sleep_ms(1000)
```

 