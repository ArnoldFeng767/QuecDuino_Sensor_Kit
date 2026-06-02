from machine import Pin
import utime

class LED(object):
    def __init__(self,pin):
        self.pin=Pin(pin,Pin.OUT,Pin.PULL_DISABLE,0)
    def write(self,value):
        self.pin.write(value)
        
    def read(self):
        return self.pin.read()
    
    def open_LED(self):
        self.pin.write(1)
        
    def close_LED(self):
        self.pin.write(0)

    def test_led(self):
        while True:
            self.open_LED()
            utime.sleep(1)
            self.close_LED()
            utime.sleep(1)


if __name__=='__main__':
    laser=LED(Pin.GPIO31)
    laser.test_led()
        