from machine import Pin
import utime


# Configure GPIO as input with pull-up functionality
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

def main():
# Assume that when the sensor detects a change in the magnetic field, it outputs a low level (0).
    while True:
        if gpio.read() == 0:
            print("Magnetic field change detected")
        else:
            print("No magnetic field change detected")
        utime.sleep(1)
if __name__ == "__main__":
    main()