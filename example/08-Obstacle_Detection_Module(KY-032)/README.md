# 障碍物检测模块

## **一、** **模块介绍**

障碍物检测模块是红外反射式数字检测器件，也叫红外避障模块，用于近距离障碍物检测、循迹、避障、限位触发；通过红外发射与接收判断前方是否有障碍物，具备响应快、体积小、3.3V/5V 兼容、GPIO 直读、抗干扰强、寿命长等优点。

**模块组成：**

![](../../media/obstacle1.png)

**工作原理：**

工作原理是红外光 线发射管**发射红外光线**，红外光线接收管**接收红外光线**，当**没有接收到返回的红外光线**时，OUT引脚输出**高电平**，当**接收到返回的红外光线时**，OUT引脚输出**低电平**。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设      | 开发板       |
| --------- | ------------ |
| 模块（+） | 3.3V         |
| 模块（-） | GND          |
| 模块（S） | PIN4(GPIO31) |

![](../../media/obstacle2.png)

## 三、 驱动代码

```python
from machine import Pin, ExtInt
import utime


class ObstacleSensor(object):
    """红外避障传感器类（KY-032），支持轮询和中断两种检测模式。

    传感器输出逻辑：
        - 无障碍物时 OUT 输出高电平 (1)
        - 检测到障碍物时 OUT 输出低电平 (0)

    应用场景：智能小车避障、自动门感应、限位检测、智能垃圾桶等。
    """

    def __init__(self, pin=Pin.GPIO31, pull=Pin.PULL_PU):
        """初始化避障传感器实例。

        Args:
            pin: GPIO 引脚号，默认 GPIO31
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.obstacle_flag = False
        self._extint = None

    def read_state(self):
        """读取当前传感器状态。"""
        return self.gpio.read()

    def is_obstacle(self):
        """判断当前是否有障碍物。"""
        return self.read_state() == 0

    def _irq_handler(self, args):
        """中断回调函数，检测到障碍物时置位标志。"""
        if self.gpio.read() == 0:
            self.obstacle_flag = True

    def monitor_polling(self, interval_ms=200):
        """轮询模式：循环读取传感器状态。

        适用于对实时性要求不高的场景，如限位检测、定期巡检。
        """
        print("[ObstacleSensor] 轮询模式启动")
        while True:
            if self.is_obstacle():
                print("检测到障碍物")
            else:
                print("无障碍物")
            utime.sleep_ms(interval_ms)

    def monitor_interrupt(self, interval_ms=200):
        """中断模式：障碍物出现时触发中断，主循环检查标志位。

        适用于需要快速响应的场景，如智能小车避障。
        """
        self._extint = ExtInt(self.gpio, ExtInt.IRQ_FALLING, Pin.PULL_PU, self._irq_handler)
        self._extint.enable()
        print("[ObstacleSensor] 中断模式启动")
        while True:
            if self.obstacle_flag:
                print("检测到障碍物")
                self.obstacle_flag = False
            else:
                print("无障碍物")
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = ObstacleSensor(pin=Pin.GPIO31)

    # 轮询模式
    sensor.monitor_polling(interval_ms=200)

    # 中断模式（取消注释以切换）
    # sensor.monitor_interrupt(interval_ms=200)
```

 