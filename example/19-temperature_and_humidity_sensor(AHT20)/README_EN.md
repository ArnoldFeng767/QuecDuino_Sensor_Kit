# Temperature and Humidity Sensor

## 1. Module Introduction

As one of the common sensors, the temperature and humidity sensor is a sensor device equipped with humidity-sensitive and temperature-sensitive elements, which can be used to measure temperature and humidity. Its working principle is mainly based on the characteristics of thermistors and humidity-sensitive resistors. It realizes accurate monitoring of environmental temperature and humidity by measuring resistance values and converting them into voltage signal outputs.

**Working Principle**:

The module collects environmental data through internal temperature-sensitive and humidity-sensitive elements, outputs **I2C digital signals** after chip calibration, and the development board reads temperature and humidity values through the I2C bus.

## 2. Connection Example

Connect the peripheral to the development board one-to-one according to the table and picture instructions:

| Peripheral   | Development Board |
| ------------ | ----------------- |
| AHT20（+）   | 3.3V              |
| AHT20（-）   | GND               |
| AHT20（SCL） | PIN17（SCL）      |
| AHT20（SDA） | PIN16（SDA）      |

![](../../media/aht20.png)

## 3.Driver Code

```python
from machine import I2C
from utime import sleep_ms


class AHT20(object):
    """AHT20 temperature and humidity sensor class, reads temperature and
    humidity data via I2C.

    Application scenarios: environmental monitoring, smart home climate
    control, warehouse temperature and humidity management, etc.
    """

    def __init__(self):
        """Initialize AHT20 sensor instance, configure I2C communication."""
        self.i2c = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        self.slave_addr = 0x38  # AHT20 I2C slave address
        self.RESET_CMD = b'\xBA'       # Reset command
        self.INIT_CMD = b'\xE1'       # Initialize command
        self.MEASURE_CMD = b'\xAC\x33\x00'  # Measurement command

    def reset(self):
        """Perform a soft reset on the sensor."""
        self.i2c.write(self.slave_addr, b'\x00', 0, self.RESET_CMD, len(self.RESET_CMD))
        sleep_ms(20)  # Wait for reset to complete

    def init(self):
        """Initialize the sensor, configure calibration parameters."""
        self.i2c.write(self.slave_addr, b'\x00', 0, self.INIT_CMD, len(self.INIT_CMD))

    def read(self):
        """Read temperature and humidity data.

        Sends measurement command, waits at least 80ms, reads 6 bytes
        and converts:
            Humidity = RH_reg / 2^20 * 100 (%)
            Temperature = temp_reg / 2^20 * 200 - 50 (C)

        Returns:
            tuple or (): (humidity, temperature), empty tuple when busy
        """
        # Send measurement command
        self.i2c.write(self.slave_addr, b'\x00', 0, self.MEASURE_CMD, len(self.MEASURE_CMD))

        # Wait for data ready (at least 80ms)
        sleep_ms(80)
        r_data = bytearray([0x00] * 6)
        self.i2c.read(self.slave_addr, b'\x00', 0, r_data, 6, 80)

        busy = 0
        if not busy:
            # Humidity data: [1] 8 bits + [2] 8 bits + [3] high 4 bits = 20 bits
            RH_reg_data = (r_data[1] << 12) | (r_data[2] << 4) | (r_data[3] >> 4)
            RH = RH_reg_data / (1 << 20) * 100

            # Temperature data: [3] low 4 bits + [4] 8 bits + [5] 8 bits = 20 bits
            temp_reg_data = ((r_data[3] & 0x0F) << 16) | (r_data[4] << 8) | r_data[5]
            temp = temp_reg_data / (1 << 20) * 200 - 50

            return RH, temp
        else:
            return ()

    def check_comfort(self, temp, rh):
        """Judge comfort level based on temperature and humidity.

        Application scenarios: smart home climate control, office environment
        monitoring, warehouse environment management, etc.

        Args:
            temp: Temperature in C
            rh: Humidity in %

        Returns:
            str: Comfort level description
        """
        if temp < 18:
            return "Cold"
        elif temp > 28:
            return "Hot"
        elif rh < 30:
            return "Dry"
        elif rh > 70:
            return "Humid"
        else:
            return "Comfortable"

    def monitor(self, interval_ms=1000):
        """Continuously monitor temperature and humidity with comfort output.

        Args:
            interval_ms: Sampling interval in milliseconds, default 1000ms
        """
        self.init()
        sleep_ms(1000)
        while True:
            res = self.read()
            if res:
                rh, temp = res
                comfort = self.check_comfort(temp, rh)
                print("Temp: %.1fC | Humidity: %.1f%% | Status: %s" % (temp, rh, comfort))
            else:
                print("Read failed")
            sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = AHT20()
    sensor.monitor(interval_ms=1000)
```



