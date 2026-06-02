# Mercury switch module

## **1. Module Introduction** 
The mercury switch module is a **gravity-sensing inclination/dumping detection digital switch device**, also known as tilt switch, angle sensor, and is commonly used in scenarios such as inclination alarm, anti-dumping protection, attitude detection, and trigger control; it relies on the flow of mercury to conduct / disconnect the circuit, output stable high or low levels, and has the advantages of **high sensitivity, reliable conduction, no mechanical contact noise, 3.3V/5V compatibility, GPIO direct reading, and small size**. 
**Luminous Principle: ** 
The module has a positive pole, a negative pole and a signal terminal. By taking advantage of the conductivity and fluidity of mercury, when tilted at a certain angle, the mercury flows and connects the electrodes, allowing the circuit to conduct; after resetting, the mercury leaves the electrodes and the circuit is disconnected. The development board determines the tilt state by reading the level.

## 2. Connection Examples 
According to the instructions provided in the table and the pictures, connect each peripheral device to the development board one by one.

| peripheral  | development board |
| ----------- | ----------------- |
| module（+） | 3.3V              |
| module（-） | GND               |
| module（S） | PIN4(GPIO31)      |

![](../../media/mercury1.png)

## 3. Driving Code

```python
from machine import Pin
import utime

class MercurySwitch:
    """Mercury switch sensor encapsulation class."""

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU):
        self.sensor = Pin(sensor_pin, Pin.IN, pull)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        return self.sensor.read()

    def is_triggered(self):
        return self.read_state() == self.trigger_level

    def update(self):
        if self.is_triggered():
            self.output.write(1)
            print("Mercury detected inclination")
        else:
            self.output.write(0)
            print("Mercury did not detect inclination")

    def monitor(self):
        while True:
            self.update()
            utime.sleep(1)

def main():
    mercury = MercurySwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU)
    mercury.monitor()

if __name__ == '__main__':
    main()

```

 