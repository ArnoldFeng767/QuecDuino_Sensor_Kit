# 水银开关模块

## **一、** **模块介绍**

水银开关模块是**重力感应式倾斜 / 倾倒检测数字开关器件**，也叫倾侧开关、角度传感器，常用于倾斜报警、防倒保护、姿态检测、触发控制场景；依靠水银流动导通 / 断开电路，输出稳定高低电平，具有**灵敏度高、导通可靠、无机械触点噪音、3.3V/5V 兼容、GPIO 直读、体积小巧**等优点。

**发光原理：**

模块有正极、负极、信号端。利用水银的导电性与流动性，倾斜到一定角度时，水银流动接通电极，电路导通；复位后水银离开电极，电路断开，开发板通过读取电平判断倾斜状态。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设          | 开发板       |
| ------------- | ------------ |
| 水银开关（+） | 3.3V         |
| 水银开关（-） | GND          |
| 水银开关（S） | PIN4(GPIO31) |

![](../../media/mercury1.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class MercurySwitch(object):
    """水银开关传感器类，检测倾斜状态并联动输出。

    应用场景：倾覆报警、跌落检测、防盗装置等。
    水银开关倾斜到一定角度时导通，输出触发电平。
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU):
        """初始化水银开关传感器实例。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，1 = 高电平触发，0 = 低电平触发，默认 1
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.sensor = Pin(sensor_pin, Pin.IN, pull)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self.sensor.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到倾斜）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_state() == self.trigger_level

    def update(self):
        """根据倾斜状态更新联动输出。"""
        if self.is_triggered():
            self.output.write(1)
            print("水银开关检测到倾斜")
        else:
            self.output.write(0)
            print("水银开关未检测到倾斜")

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测倾斜状态并联动输出。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            self.update()
            utime.sleep(interval_sec)


if __name__ == '__main__':
    mercury = MercurySwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1, pull=Pin.PULL_PU)
    mercury.monitor(interval_sec=1)
```

 