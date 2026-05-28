from machine import Pin
import utime

led=Pin(Pin.GPIO31,Pin.OUT,Pin.PULL_DISABLE,1)

while True:
    led.write(0)
    utime.sleep(1)
    led.write(1)
    utime.sleep(1)