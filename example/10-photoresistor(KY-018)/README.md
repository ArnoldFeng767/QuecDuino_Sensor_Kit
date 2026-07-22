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

    传感器特性：光照越强，ADC 值越低；光照越弱，ADC 值越高。

    Args:
        adc_channel:    ADC 通道，默认 ADC1
        led_pin:        LED 指示 GPIO，默认 GPIO31，传 None 禁用
        dark_threshold: 低于此值判定为暗，默认 200
        led_mode:       'dark'=暗时亮灯(自动路灯), 'bright'=亮时亮灯, 'off'=不控灯
        sample_ms:      采样间隔 ms，默认 500
    """

    MODE_DARK = 'dark'
    MODE_BRIGHT = 'bright'
    MODE_OFF = 'off'

    def __init__(self, adc_channel=None, led_pin=Pin.GPIO31,
                 dark_threshold=200, led_mode='bright', sample_ms=500):
        self._dark_threshold = dark_threshold
        self._led_mode = led_mode
        self._sample_ms = sample_ms
        self._led = None
        if led_pin is not None:
            self._led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0

    def set_callback(self, callback):
        """设置光照变化回调。

        Args:
            callback: 回调函数，签名 callback(adc_value, is_dark)
        """
        self._callback = callback

    @property
    def dark_threshold(self):
        return self._dark_threshold

    @dark_threshold.setter
    def dark_threshold(self, value):
        self._dark_threshold = value

    def read_value(self):
        """读取当前光照强度 ADC 值。"""
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_dark(self):
        """判断当前环境是否偏暗。"""
        return self._last_value > self._dark_threshold

    def _update_led(self, value):
        """根据 led_mode 更新 LED 状态。"""
        if self._led is None or self._led_mode == self.MODE_OFF:
            return
        dark = value > self._dark_threshold
        if self._led_mode == self.MODE_DARK:
            self._led.write(1 if dark else 0)
        elif self._led_mode == self.MODE_BRIGHT:
            self._led.write(0 if dark else 1)

    def _monitor(self):
        """后台监控循环。"""
        while self._is_running:
            value = self.read_value()
            dark = self.is_dark()
            self._update_led(value)
            print("光照: {} | {}".format(value, "暗" if dark else "亮"))
            if self._callback:
                self._callback(value, dark)
            utime.sleep_ms(self._sample_ms)

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """停止后台监控线程并关闭 LED。"""
        self._is_running = False
        if self._led is not None:
            self._led.write(0)


if __name__ == '__main__':
    lc = LightController(led_pin=Pin.GPIO31, dark_threshold=200,
                         led_mode=LightController.MODE_DARK, sample_ms=500)
    lc.start()

    while True:
        utime.sleep_ms(1000)
```

