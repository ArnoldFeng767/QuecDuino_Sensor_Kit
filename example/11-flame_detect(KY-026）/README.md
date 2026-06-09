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

### 模拟信号（ADC 模式）

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class FlameSensor(object):
    """火焰传感器类（ADC 模式），通过模拟量读取火焰强度并分级报警。

    分级逻辑：
        - ADC < 100：无火焰
        - 100 <= ADC < 500：火险隐患，LED 常亮
        - ADC >= 500：火灾，LED 快闪
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31):
        """初始化火焰传感器实例（ADC 模式）。

        Args:
            adc_channel: ADC 通道，默认使用 ADC0
            led_pin: LED 报警指示灯 GPIO 引脚号，默认 GPIO31
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC0 if adc_channel is None else adc_channel
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_value(self):
        """读取当前火焰强度 ADC 值。"""
        return self.adc.read(self.adc_channel)

    def led_blink(self):
        """LED 快闪，用于火灾报警指示。"""
        self.led.write(1)
        utime.sleep(0.5)
        self.led.write(0)
        utime.sleep(0.5)

    def monitor(self):
        """后台监控循环，根据火焰强度分级响应。"""
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if value < 100:
                self.led.write(0)
                print("ADC: {} | 状态: 安全".format(value))
            elif value < 500:
                self.led.write(1)
                print("ADC: {} | 状态: 火险隐患".format(value))
            else:
                self.led_blink()
                print("ADC: {} | 状态: 火灾报警".format(value))
            utime.sleep(1)

    def start(self):
        """启动后台监控线程。"""
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    flame_sensor = FlameSensor()
    flame_sensor.start()

    while True:
        utime.sleep_ms(1000)
```

### 数字信号（GPIO 模式）

```python
from machine import Pin
import utime


class FlameDigitalSensor(object):
    """火焰传感器类（GPIO 模式），通过数字量检测火焰并联动输出。

    应用场景：火灾报警、火源检测、安全监控等。
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        """初始化火焰传感器实例（GPIO 模式）。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，默认 1（高电平触发）
        """
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.last_state = self.sensor.read()

    def read_state(self):
        """读取传感器当前电平状态。"""
        return self.sensor.read()

    def is_flame_detected(self):
        """判断当前是否检测到火焰。"""
        return self.read_state() == self.trigger_level

    def set_output(self, active):
        """控制联动输出引脚，可驱动 LED、蜂鸣器等。"""
        self.output.write(1 if active else 0)

    def update(self):
        """根据传感器状态更新联动输出，并返回状态变化信息。"""
        state = self.read_state()
        detected = state == self.trigger_level
        self.set_output(detected)

        if detected:
            print("检测到火焰")

        changed = state != self.last_state
        self.last_state = state
        return changed, detected

    def monitor(self, interval_ms=100):
        """轮询监控循环，检测火焰状态并联动输出。"""
        while True:
            self.update()
            utime.sleep_ms(interval_ms)


if __name__ == "__main__":
    flame_sensor = FlameDigitalSensor(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    flame_sensor.monitor()
```

``    

 