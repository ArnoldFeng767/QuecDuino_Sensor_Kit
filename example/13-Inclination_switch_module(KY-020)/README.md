# 倾斜开关模块

## **一、** **模块介绍**

倾斜开关是**姿态感应数字开关器件**，也被称作滚珠开关、倾倒传感器，常用于倾斜检测、防倒保护、姿态触发、智能报警场景；它能在模块倾斜到一定角度时自动切换电平信号，具备体积小、无触点、低功耗、3.3V/5V 兼容、直接 GPIO 检测、响应灵敏、寿命长等优点。

**工作原理：**

模块有正极、负极、信号端。倾斜时内部滚珠 / 导电液移动，使内部触点导通或断开，输出高低电平，开发板可直接读取状态判断是否倾斜。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设          | 开发板       |
| ------------- | ------------ |
| 倾斜开关（+） | 3.3V         |
| 倾斜开关（-） | GND          |
| 倾斜开关（S） | PIN4(GPIO31) |

![](../../media/lnclination1.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class InclinationSwitch(object):
    """倾斜开关传感器类，通过 GPIO 检测倾斜状态并控制 LED 指示。

    应用场景：倾覆报警、设备姿态检测、运输振动指示等。
    """

    def __init__(self, pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU):
        """初始化倾斜开关传感器实例。

        Args:
            pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            led_pin: LED 指示灯 GPIO 引脚号，默认 GPIO32
            trigger_level: 触发电平，默认 0（低电平触发）
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.led = Pin(led_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        """读取传感器当前电平状态。"""
        return self.gpio.read()

    def is_tilted(self):
        """判断当前是否处于倾斜状态。"""
        return self.read_state() == self.trigger_level

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测倾斜状态并控制 LED。"""
        while True:
            if self.is_tilted():
                self.led.write(1)
                print("检测到倾斜")
            else:
                self.led.write(0)
                print("水平状态")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    tilt_switch = InclinationSwitch(pin=Pin.GPIO31, led_pin=Pin.GPIO32, trigger_level=0, pull=Pin.PULL_PU)
    tilt_switch.monitor(interval_sec=1)
```
