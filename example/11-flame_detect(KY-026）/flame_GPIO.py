from machine import Pin,ExtInt
import utime


#Configure GPIO as input with pull-down
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PD)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)
def main():
    # When the sensor detects a flame, it outputs a high level (1).
    while True:
        if gpio.read() == 0:
            gpio1.write(0)
        else:
            gpio1.write(1)
            print("Flames were detected.")
        utime.sleep_ms(100)
if __name__ == "__main__":
    main()
        