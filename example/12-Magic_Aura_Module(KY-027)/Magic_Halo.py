
from machine import Pin,ExtInt
import utime

# Global flag
human_detected = False

# Configure GPIO as input with pull-down
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PD)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)

def main():
    # When the sensor detects an inclination, it outputs a high level (1).
    while True:
        if gpio.read() == 1:
            print("Mercury detected inclination")
            gpio1.write(1)
        else:
            print("Mercury did not detect inclination")
            gpio1.write(0)
        utime.sleep(1)
        

if __name__ == '__main__':
    main()

