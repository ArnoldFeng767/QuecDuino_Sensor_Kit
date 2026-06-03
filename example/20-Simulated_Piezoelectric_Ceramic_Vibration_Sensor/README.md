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


class VibrationSensor:
    """Vibration sensor encapsulation class."""

    def __init__(self, adc_channel=None, alert_threshold=1500):
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.alert_threshold = alert_threshold
        self.is_running = False

    def open(self):
        self.adc.open()

    def read_value(self):
        # The larger the value, the stronger the impact/vibration is usually indicated.
        return self.adc.read(self.adc_channel)

    def check_alert(self, value):
        # Actual application: cabinet tamper detection, device drop detection, door/window vibration alarm.
        return value >= self.alert_threshold
    def monitor(self):
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if self.check_alert(value):
                print("Vibration alert, value = {}".format(value))
            else:
                print("Vibration value = {}".format(value))
            utime.sleep_ms(200)

    def start(self):
        self.open()
        _thread.start_new_thread(self.monitor, ())

    def stop(self):
        self.is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500)
    sensor.start()

    while True:
        utime.sleep_ms(1000)
```

 