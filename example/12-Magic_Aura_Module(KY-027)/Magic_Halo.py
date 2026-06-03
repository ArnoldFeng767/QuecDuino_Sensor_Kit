"""
@file      : Magic_Halo.py
@author    : Aaron Chen
@brief     : Simple class-based tilt sensor example
@version   : 0.1
@date      : 2026-06-02
"""

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

