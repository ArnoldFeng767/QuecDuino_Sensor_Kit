# 人体触摸模块

## **一、** **模块介绍**

该模块是一个基于触摸检测的电容式点动型触摸开关模块。·金属触摸模块是通过人体的电容来作出反应的。由于其是监测电容，还可以在模块表面覆盖非金属材料如木材、纸、塑料等等jue缘材料，来检测人的触摸可做成隐藏在墙壁、桌面等地方的按键。

**模块组成：**

![](../../media/finger1.png) 

**发光原理：**

模块有正极、负极、信号端。人体触摸感应片时，电容值发生变化，模块内部电路识别后输出高低电平信号，开发板可直接读取状态判断是否被触摸。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设      | 开发板       |
| --------- | ------------ |
| 模块（+） | 3.3V         |
| 模块（-） | GND          |
| 模块（S） | PIN4(GPIO31) |

![](../../media/finger2.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class TouchSensor(object):
    """人体触摸传感器类，通过 GPIO 检测触摸状态。

    典型用法:
        ts = TouchSensor(pin=Pin.GPIO31)
        ts.set_callback(lambda t: print("触摸!" if t else "释放"))
        ts.monitor()

    Args:
        pin:          传感器输入 GPIO，默认 GPIO31
        trigger_level: 触发电平，默认 1（高电平触发）
        pull:          上下拉配置，默认下拉 (Pin.PULL_PD)
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """设置触摸状态变化回调。callback(is_touched)"""
        self._callback = callback

    def read_state(self):
        """读取传感器当前电平状态。"""
        return self._gpio.read()

    def is_touched(self):
        """判断当前是否被触摸。"""
        return self.read_state() == self._trigger_level

    @property
    def trigger_count(self):
        """获取累计触摸次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触摸计数归零。"""
        self._trigger_count = 0

    def wait_for_touch(self, timeout_ms=None):
        """阻塞等待触摸。"""
        start = utime.ticks_ms()
        while True:
            if self.is_touched():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def monitor(self, interval_sec=1):
        """轮询监控循环。"""
        while True:
            state = self.read_state()
            touched = state == self._trigger_level
            changed = touched != (self._last_state == self._trigger_level)
            self._last_state = state
            if changed:
                if touched:
                    self._trigger_count += 1
                if self._callback:
                    self._callback(touched)
                print("检测到触摸" if touched else "触摸释放")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    ts = TouchSensor(pin=Pin.GPIO31, trigger_level=1, pull=Pin.PULL_PD)
    ts.monitor(interval_sec=1)
```

