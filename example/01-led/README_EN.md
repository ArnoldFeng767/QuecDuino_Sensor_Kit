# LED module

## **1. Module Introduction**

LED Principles and Industry Classification: LED is the abbreviation for Light Emitting Diode (Light Emitting Diode, LED), also known as light-emitting diode. Since its development, this semiconductor component has generally been used as indicator lights and display panels. However, with the advancement of technology, it can now be used as a light source. It not only can directly convert electrical energy into light energy with high efficiency, but also has a lifespan of up to tens of thousands to 100,000 hours. At the same time, it is less fragile than traditional bulbs, can save electricity, is environmentally friendly without mercury, has a small size, can be applied in low-temperature environments, has directional light, causes less light pollution, and has a rich color gamut.

**LED Composition:**

![](../../media/led1.png)

**Luminous Principle:**

![](../../media/led2.png)

On the left is the positive pole, and on the right is the negative pole. When a voltage difference is formed between the positive and negative poles, the LED lights up.

## 2. Connection Examples

According to the instructions provided in the table and pictures, connect the peripherals one by one to the development board.

| peripheral | development board |
| ---------- | ----------------- |
| LED（+）   | 3.3V              |
| LED（-）   | GND               |
| LED（S）   | PIN4(GPIO31)      |

 

![](../../media/led3.png)

## 3. Driving Code

```python
from machine import Pin
import utime

class LED():
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
        
        
```

 