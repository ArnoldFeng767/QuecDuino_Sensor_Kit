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

    应用场景：机柜防拆检测、设备跌落检测、门窗振动报警等。
    ADC 值越大表示振动/冲击越强。
    """

    def __init__(self, adc_channel=None, alert_threshold=1500):
        """初始化振动传感器实例。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            alert_threshold: 振动报警阈值，ADC 值超过此值触发报警，默认 1500
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.alert_threshold = alert_threshold
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_value(self):
        """读取当前振动强度 ADC 值。

        注意：值越大通常表示振动/冲击越强。

        Returns:
            int: ADC 采样值
        """
        return self.adc.read(self.adc_channel)

    def check_alert(self, value):
        """判断振动是否超过报警阈值。

        实际应用场景：机柜防拆检测、设备跌落检测、门窗振动报警等。

        Args:
            value: 当前 ADC 采样值

        Returns:
            bool: True 表示触发报警
        """
        return value >= self.alert_threshold

    def monitor(self, interval_ms=200):
        """后台监控循环，持续采样并输出振动状态。

        Args:
            interval_ms: 采样间隔，单位毫秒，默认 200ms
        """
        self.is_running = True
        while self.is_running:
            value = self.read_value()
            if self.check_alert(value):
                print("振动报警, 数值 = {}".format(value))
            else:
                print("振动数值 = {}".format(value))
            utime.sleep_ms(interval_ms)

    def start(self, interval_ms=200):
        """启动后台监控线程。

        Args:
            interval_ms: 采样间隔，单位毫秒，默认 200ms
        """
        self.open()
        _thread.start_new_thread(self.monitor, (interval_ms,))

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    sensor = VibrationSensor(alert_threshold=1500)
    sensor.start()

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)
```

 