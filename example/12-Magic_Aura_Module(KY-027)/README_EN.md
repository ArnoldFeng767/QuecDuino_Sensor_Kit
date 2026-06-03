# Magic Halo Module

## 1. Module Introduction

The Magic Halo Module (KY‑027) is a 2-in-1 digital module integrating **tilt sensing + LED lighting**, with a built-in mercury switch and high-brightness LED. It is used for tilt detection, posture triggering, status indication, and maker interaction projects. The module features small size, fast response, digital level output, 3.3V/5V compatibility, direct GPIO driving, and stable service life.

**Working Principle**:

![](../../media/magic1.png)

The module has power supply, ground, signal output, and LED control terminals. When tilted to a certain angle, the mercury switch is turned on/off to output high/low level; the LED can be controlled to turn on/off via GPIO to achieve effects such as tilt lighting and posture alarm.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |
| Module（L） | PIN5(GPIO30)      |

![](../../media/magic2.png)

## 3.Driver Code

```python
from machine import Pin
import utime


class TiltSwitch(object):
	"""Tilt switch class, suitable for posture detection and linkage alerts."""

	def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
		# Practical applications: Tipping alarm, equipment posture detection, transportation vibration/deflection indication.
		self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
		self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
		self.trigger_level = trigger_level

	def read_state(self):
		return self.sensor.read()

	def is_tilted(self):
		return self.read_state() == self.trigger_level

	def update(self):
		if self.is_tilted():
			self.output.write(1)
			print("Tilt detected")
		else:
			self.output.write(0)
			print("Normal position")

	def monitor(self, interval_sec=1):
		while True:
			self.update()
			utime.sleep(1)

def main():
	tilt_switch = TiltSwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
	tilt_switch.monitor(1)


if __name__ == '__main__':
	main()
```

 