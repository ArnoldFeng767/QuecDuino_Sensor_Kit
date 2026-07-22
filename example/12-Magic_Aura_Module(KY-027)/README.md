# 魔术光环模块

## **一、** **模块介绍**

魔术光环模块（KY‑027）是**倾斜感应 + LED 发光**二合一数字模块，内置水银开关与高亮 LED，用于倾斜检测、姿态触发、状态指示、创客互动项目；模块体积小、响应快、数字电平输出、3.3V/5V 兼容、直接接 GPIO 驱动、寿命稳定。

**工作原理：**

![](../../media/magic1.png)

模块有供电、接地、信号输出、LED 控制端。倾斜到一定角度时，水银开关导通 / 断开，输出高低电平；可通过 GPIO 控制 LED 亮灭，实现倾斜亮灯、姿态报警等效果。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设          | 开发板       |
| ------------- | ------------ |
| 魔术光环（+） | 3.3V         |
| 魔术光环（-） | GND          |
| 魔术光环（S） | PIN4(GPIO31) |
| 魔术光环（L） | PIN5(GPIO30) |

![](../../media/magic2.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class TiltSwitch(object):
    """倾斜开关传感器类，检测设备姿态并联动输出。

    Args:
        sensor_pin:   传感器输入 GPIO，默认 GPIO31
        output_pin:   联动输出 GPIO，默认 GPIO30，传 None 禁用
        trigger_level: 1=高电平触发，0=低电平触发，默认 1
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        self._sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._last_state = self._sensor.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """设置状态变化回调。callback(is_tilted)"""
        self._callback = callback

    def read_state(self):
        """读取传感器当前电平状态。"""
        return self._sensor.read()

    def is_tilted(self):
        """判断当前是否处于倾斜状态。"""
        return self.read_state() == self._trigger_level

    def set_output(self, active):
        """控制联动输出引脚。"""
        if self._output is not None:
            self._output.write(1 if active else 0)

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    def wait_for_tilt(self, timeout_ms=None):
        """阻塞等待倾斜触发。"""
        start = utime.ticks_ms()
        while True:
            if self.is_tilted():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def _check_state(self):
        state = self.read_state()
        tilted = state == self._trigger_level
        self.set_output(tilted)
        changed = state != self._last_state
        if changed and tilted:
            self._trigger_count += 1
            if self._callback:
                self._callback(True)
        elif changed and not tilted:
            if self._callback:
                self._callback(False)
        self._last_state = state
        return changed, tilted

    def monitor(self, interval_sec=1):
        """轮询监控循环。"""
        while True:
            changed, tilted = self._check_state()
            if changed:
                print("检测到倾斜" if tilted else "位置正常")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    ts = TiltSwitch(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    ts.monitor(interval_sec=1)
```
