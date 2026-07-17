# 模拟压电陶瓷震动模块

## **一、** **模块介绍**

这个传感器是基于压电陶瓷片模拟震动的传感器，它利用压电陶瓷给电信号产生震动的反变换过程。当压电陶瓷片震动时，该传感器信号端就会产生电信号。该模块兼容各种单片机控制板，如arduino系列单片机。模块包含2种接口，任你选择。一种是间距为2.54mm的防反接白色端子，使用时，我们可以在单片机上堆叠一个传感器扩展板。模块和自带导线连接，然后连接在传感器扩展板上，简单方便。另一种是间距为2.54mm的排针接口，利用公对母杜邦线，可直接连接在单片机上。

**工作原理：**

 **作为震动输出（逆压电效应）**：模块有供电、接地、信号端。当信号端输入脉冲 / 方波电信号时，压电陶瓷片因逆压电效应产生形变，带动基底振动，实现震动反馈。

**作为震动检测（正压电效应）**：当模块受到机械震动 / 敲击时，压电陶瓷片产生微弱电信号，由信号端输出，开发板通过 ADC 采集即可检测震动强度。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设      | 开发板     |
| --------- | ---------- |
| 模块（+） | 3.3V       |
| 模块（-） | GND        |
| 模块（S） | A1（ADC1） |

 

 ![](../../media/detection1.png)



## 三、 驱动代码

```python
from misc import ADC
import _thread
import utime


class VibrationSensor(object):
    """振动传感器类，通过 ADC 采集振动强度并阈值报警。

    典型用法:
        sensor = VibrationSensor(alert_threshold=1500)
        sensor.set_callback(lambda val: print("振动!", val))
        sensor.start()

    Args:
        adc_channel:    ADC 通道，默认 ADC1
        alert_threshold: 报警阈值，默认 1500
        sample_ms:      采样间隔 ms，默认 200
    """

    def __init__(self, adc_channel=None, alert_threshold=1500, sample_ms=200):
        self._alert_threshold = alert_threshold
        self._sample_ms = sample_ms
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._callback = None
        self._is_running = False
        self._last_value = 0

    def set_callback(self, callback):
        """设置振动报警回调。callback(adc_value)"""
        self._callback = callback

    @property
    def alert_threshold(self):
        return self._alert_threshold

    @alert_threshold.setter
    def alert_threshold(self, value):
        self._alert_threshold = value

    def read_value(self):
        """读取当前振动强度 ADC 值。"""
        self._last_value = self._adc.read(self._adc_channel)
        return self._last_value

    def is_alert(self, value=None):
        """判断振动是否超过报警阈值。"""
        v = value if value is not None else self._last_value
        return v >= self._alert_threshold

    def _monitor(self):
        """后台监控循环。"""
        while self._is_running:
            value = self.read_value()
            if value >= self._alert_threshold:
                print("振动报警, 数值 = {}".format(value))
                if self._callback:
                    self._callback(value)
            utime.sleep_ms(self._sample_ms)

    def start(self):
        """启动 ADC 并开启后台监控线程。"""
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, ())

    def stop(self):
        """停止后台监控线程。"""
        self._is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500, sample_ms=200)
    sensor.set_callback(lambda v: print("振动报警触发! ADC={}".format(v)))
    sensor.start()

    while True:
        utime.sleep_ms(1000)
```

 