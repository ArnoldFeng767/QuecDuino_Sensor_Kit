# 激光发射模块

## **一、** **模块介绍**

**激光发射模块（Laser Emitter Module）** 的核心原理是：**通过半导体激光二极管（LD），将电能高效转化为高亮度、高方向性、单色性的相干光（激光），再经光学系统准直 / 整形后发射出去**。它广泛用于激光测距、激光雷达、光纤通信、激光指示、红外夜视等场景。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设        | 开发板       |
| ----------- | ------------ |
| Module（+） | 3.3V         |
| Module（-） | GND          |
| Module（S） | PIN4(GPIO31) |

![](../../media/laser1.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class LaserEmitter(object):
    """激光发射器控制类，通过 GPIO 控制激光开关和闪烁。

    通过 active_level 参数适配不同触发方式。
    应用场景：激光指示、对准辅助、安防警示等。
    """

    def __init__(self, pin=Pin.GPIO31, active_level=1):
        """初始化激光发射器实例。

        Args:
            pin: GPIO 引脚号，默认 GPIO31
            active_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
        """
        self.active_level = active_level
        self.inactive_level = 0 if active_level else 1
        self.gpio = Pin(pin, Pin.OUT, Pin.PULL_DISABLE, self.inactive_level)

    def on(self):
        """开启激光。"""
        self.gpio.write(self.active_level)
        print("激光开启")

    def off(self):
        """关闭激光。"""
        self.gpio.write(self.inactive_level)
        print("激光关闭")

    def blink(self, interval=2):
        """激光闪烁一次（开→关）。

        Args:
            interval: 开关间隔，单位秒，默认 2 秒
        """
        self.on()
        utime.sleep(interval)
        self.off()
        utime.sleep(interval)

    def demo(self, interval=2):
        """演示循环，持续闪烁。

        Args:
            interval: 闪烁间隔，单位秒，默认 2 秒
        """
        while True:
            self.blink(interval)


if __name__ == '__main__':
    laser = LaserEmitter(pin=Pin.GPIO31, active_level=1)
    laser.demo(interval=2)
```

