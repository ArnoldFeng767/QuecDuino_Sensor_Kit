# Photosensitive Resistor Module

## 1. Module Introduction

The photosensitive resistor sensor is a type of sensor that can convert optical signals into electrical signals, and its resistance value changes with the intensity of light. In many practical applications, such as automatic lighting systems, ambient light detection, etc., the photosensitive resistor sensor plays an important role. The EG800Z Duino development board is equipped with rich peripheral resources, which can be easily combined with the photosensitive resistor sensor to realize the detection and processing of light intensity.

Photosensitive resistors are usually made of semiconductor materials, and their working principle is based on the internal photoelectric effect. When light irradiates the photosensitive resistor, electrons in the semiconductor material absorb the energy of photons and transition from the valence band to the conduction band, thereby enhancing the conductivity of the material and reducing the resistance value. Conversely, when the light intensity weakens, the resistance value increases.

The characteristic curve of a photosensitive resistor usually shows a non-linear relationship, that is, the relationship between light intensity and resistance value is not a simple linear proportional relationship. In practical applications, calibration and processing need to be carried out according to specific requirements and characteristic curves.

**Composition of Photosensitive Resistor:**

![](../../media/light1.png)

Working Principle:

![](../../media/light2.png)

**The stronger the light, the smaller the resistance and the lower the voltage; the weaker the light, the larger the resistance and the higher the voltage.**

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral | Development Board |
| ---------- | ----------------- |
| LDR（+）   | 3.3V              |
| LDR（-）   | GND               |
| LDR（S）   | A1（ADC1）        |

![](../../media/light3.png)

## 3.Driving Code

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class LightController(object):
    """Photoresistor controller class, reads light intensity via ADC and controls LED.

    Sensor characteristic: stronger light → lower ADC value.

    Example:
        # Auto street light mode: LED on when dark
        lc = LightController(led_pin=Pin.GPIO31, dark_threshold=200, led_mode='dark')
        lc.start()

    Args:
        adc_channel:    ADC channel, default ADC1
        led_pin:        LED GPIO pin, default GPIO31, pass None to disable
        dark_threshold: ADC value above which is considered dark, default 200
        led_mode:       'dark'=on when dark, 'bright'=on when bright, 'off'=no LED control
        sample_ms:      sampling interval in ms, default 500
    """

    MODE_DARK = 'dark'
    MODE_BRIGHT = 'bright'
    MODE_OFF = 'off'

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 dark_threshold=200, led_mode='bright', sample_ms=500):
        self._dark_threshold = dark_threshold
        self._led_mode = led_mode
        self._sample_ms = sample_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0

    def set_callback(self, callback):
        """Set light change callback.

        Args:
            callback: function with signature callback(adc_value, is_dark)
        """
        self._callback = callback

    @property
    def dark_threshold(self):
        return self._dark_threshold

    @dark_threshold.setter
    def dark_threshold(self, value):
        self._dark_threshold = value

    def read_value(self):
        """Read current light intensity ADC value."""
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_dark(self):
        """Check if current environment is dark."""
        return self._last_value > self._dark_threshold

    def _update_led(self, value):
        """Update LED based on led_mode."""
        if self._led is None or self._led_mode == self.MODE_OFF:
            return
        dark = value > self._dark_threshold
        if self._led_mode == self.MODE_DARK:
            self._led.write(1 if dark else 0)
        elif self._led_mode == self.MODE_BRIGHT:
            self._led.write(0 if dark else 1)

    def _monitor(self):
        """Background monitoring loop."""
        while self._is_running:
            value = self.read_value()
            dark = self.is_dark()
            self._update_led(value)
            print("Light: {} | {}".format(value, "Dark" if dark else "Bright"))
            if self._callback:
                self._callback(value, dark)
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
    lc = LightController(led_pin=Pin.GPIO31, dark_threshold=200,
                         led_mode=LightController.MODE_DARK, sample_ms=500)
    lc.start()

    while True:
        utime.sleep_ms(1000)
```

