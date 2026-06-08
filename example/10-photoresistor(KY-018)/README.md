# 光敏电阻模块

## **一、** **模块介绍**

光敏电阻传感器是一种能够将光信号转换为电信号的传感器，其阻值会随着光照强度的变化而改变。在许多实际应用中，如自动照明系统、环境光检测等，光敏电阻传感器发挥着重要作用。 EG800Z Duino开发板具有丰富的外设资源，能够方便地与光敏电阻传感器结合使用，实现对光照强度的检测和处理。

光敏电阻通常由半导体材料制成，其工作原理基于内光电效应。当光线照射到光敏电阻上时，半导体材料中的电子会吸收光子的能量，从价带跃迁到导带，从而使材料的导电能力增强，电阻值降低。反之，当光照强度减弱时，电阻值会增大。

光敏电阻的特性曲线通常呈现出非线性 关系，即光照强度与电阻值之间不是简单的线性比例关系。在实际应用中，需要根据具体的需求和特性曲线来进行校准和处理。

**光敏电阻组成：**

![](../../media/light1.png)

**工作原理：**

![](../../media/light2.png)

**光照越强，电阻越小，电压越低；光照越弱，电阻越大，电压越高。**

## 二、连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设     | 开发板     |
| -------- | ---------- |
| LDR（+） | 3.3V       |
| LDR（-） | GND        |
| LDR（S） | A1（ADC1） |

![](../../media/light3.png)

## 三、 驱动代码

```python
from misc import ADC
from machine import Pin
import _thread
import utime


class LightController(object):
    """光敏电阻控制器类，通过 ADC 读取光照强度并控制 LED。

    传感器特性：光照越强，电阻越小，ADC 值越低；光照越弱，电阻越大，ADC 值越高。
    应用场景：自动路灯、智能照明、环境光检测等。
    """

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31, sample_ms=500):
        """初始化光敏电阻控制器。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            led_pin: LED 指示灯 GPIO 引脚号，默认 GPIO31
            sample_ms: 采样间隔，单位毫秒，默认 500ms
        """
        self.sample_ms = sample_ms
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.is_running = False

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self.adc.open()
        self.is_running = True
        _thread.start_new_thread(self.monitor, ())

    def monitor(self):
        """后台监控循环，读取光照强度并根据阈值控制 LED。

        注意：当前逻辑为演示用途（光线弱关灯，光线强开灯）。
        实际自动路灯场景应反转逻辑：光线弱 → 开灯，光线强 → 关灯。
        """
        while self.is_running:
            light_value = self.adc.read(self.adc_channel)
            print("光照强度值: {}".format(light_value))
            if light_value < 50:
                self.led.write(0)
                print("光线弱，关闭 LED")
            else:
                self.led.write(1)
                print("光线强，开启 LED")
            utime.sleep_ms(self.sample_ms)

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    light_controller = LightController(
        led_pin=Pin.GPIO31,
        sample_ms=500,
    )
    light_controller.start()

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)
```

