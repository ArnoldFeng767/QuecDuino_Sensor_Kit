# 火焰检测模块

## **一、** **模块介绍**

火焰检测模块是用于**探测火焰 / 明火**的传感器模块，通过接收火焰产生的红外光，输出高低电平信号，实现火灾报警、火源检测。

**核心参数**

- 工作电压：3.3V–5V
- 输出：数字信号（无高 /有低）
- 输出：模拟信号（近高 / 远低）
- 检测角度：约 60°
- 接口：**MX1.25-2P**
- 用途：火焰检测、火灾报警、火源判断

## 二、连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设         | 开发板                   |
| ------------ | ------------------------ |
| Flame（+）   | 3.3V                     |
| Flame（-）   | GND                      |
| Flame（A/D） | A1（ADC1）/ PIN4(GPIO31) |

![](../../media/flame1.png)

## 三、 驱动代码

`模拟信号`

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class FlameSensor(object):
    """Flame sensor packaging class."""

    def __init__(self, adc_channel=None,pin=Pin.GPIO31):
        self.adc = ADC()
        self.adc_channel = self.adc.ADC0 if adc_channel is None else adc_channel
        self.led=Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.is_running = False

    def open(self):
        self.adc.open()

    def read_value(self):
        return self.adc.read(self.adc_channel)

    def led_link(self):
        self.led.write(1)
        utime.sleep(0.5)
        self.led.write(0)
        utime.sleep(0.5)
    def monitor(self):
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            print(value)
            if value > 100 and value < 500:
                self.led.high()
                self.led.write(1)
                print("There is a fire hazard.")
            elif value > 500:
                self.led_link()
                print("There is a fire.")
            utime.sleep(1)

    def start(self):
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    flame_sensor = FlameSensor()
    flame_sensor.start()

    while True:
        utime.sleep_ms(1000)
```



`数字信号`

```python
from machine import Pin
import utime


class FlameDigitalSensor:
    """数字火焰传感器封装类。"""

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.last_state = self.sensor.read()

    def read_state(self):
        return self.sensor.read()

    def is_flame_detected(self):
        return self.read_state() == self.trigger_level

    def set_output(self, active):
        self.output.write(1 if active else 0)
    def update(self):
        state = self.read_state()
        detected = state == self.trigger_level
        self.set_output(detected)

        if detected:
            print("Flames were detected.")

        changed = state != self.last_state
        self.last_state = state
        return changed, detected

    def monitor(self):
        while True:
            self.update()
            utime.sleep_ms(100)


def main():
    flame_sensor = FlameDigitalSensor(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    flame_sensor.monitor()


if __name__ == "__main__":
    main()
```

``    

 