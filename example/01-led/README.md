# LED模块

## **一、** **模块介绍**

LED原理及产业分类LED是发光二极体( Light EmitTIng Diode, LED)的简称，也被称作发光二极管，这种半导体组件发展以来一般是作为指示灯、显示板，但目前随着技术增加，已经能作为光源使用，它不但能够高效率地直接将电能转化为光能，而且拥有最长达数万小时～10 万小时的使用寿命，同时具备不若传统灯泡易碎，并能省电，同时拥有环保无汞、体积小、可应用在低温环境、光源具方向性、造成光害少与色域丰富等优点。

**LED组成：**

![](../../media/led1.png)

**发光原理：**

![](../../media/led2.png)

左为正极，右为负极。当正负极形成电压差时，LED点亮。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设     | 开发板       |
| -------- | ------------ |
| LED（+） | 3.3V         |
| LED（-） | GND          |
| LED（S） | PIN4(GPIO31) |

 

![](../../media/led3.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class LED(object):
    """LED 控制类，封装 GPIO 引脚对 LED 的基本操作。

    Args:
        pin: GPIO 引脚号，例如 Pin.GPIO31
    """

    def __init__(self, pin):
        # 初始化 GPIO 为输出模式，禁用上下拉电阻，默认低电平（LED 熄灭）
        self.pin = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, 0)

    def write(self, value):
        """设置 LED 的电平状态。

        Args:
            value: 1 表示高电平（点亮），0 表示低电平（熄灭）
        """
        self.pin.write(value)

    def read(self):
        """读取当前 LED 引脚的电平状态。

        Returns:
            int: 1 或 0
        """
        return self.pin.read()

    def on(self):
        """点亮 LED（输出高电平）。"""
        self.pin.write(1)

    def off(self):
        """熄灭 LED（输出低电平）。"""
        self.pin.write(0)

    def blink(self, interval=1):
        """LED 闪烁，以指定间隔循环亮灭。

        Args:
            interval: 亮灭切换间隔，单位秒，默认 1 秒
        """
        while True:
            self.on()
            utime.sleep(interval)
            self.off()
            utime.sleep(interval)


if __name__ == '__main__':
    # 使用 GPIO31 引脚创建 LED 实例
    led = LED(Pin.GPIO31)
    # 运行闪烁测试（每秒切换一次）
    led.blink()
```

 