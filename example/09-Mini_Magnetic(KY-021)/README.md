# 迷你磁簧模块

## **一、** **模块介绍**

迷你磁簧，全称**迷你磁簧开关（干簧管模块）**，是一种利用磁场控制通断的无源开关组件，这类磁性感应器件一般作为门磁检测、位置检测、限位触发使用，目前已经广泛用于嵌入式设备、智能硬件、创客 DIY 场景；它能够在磁场靠近时导通、磁场远离时断开，拥有体积小、响应快、无机械触点磨损、低功耗、即插即用、适配 3.3V/5V 低压环境、可直接接 GPIO 检测、使用寿命长等优点。

迷你磁环组成：

![](../../media/mini1.png)

**工作原理：**

模块本质是一个受磁场控制的开关。当磁铁靠近模块时，玻璃管内的磁簧片被磁化并相互吸引接触，电路导通；当磁铁远离时，簧片失去磁性并依靠弹性分离，电路断开，以此实现磁场触发的开关信号输出。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设      | 开发板       |
| --------- | ------------ |
| 磁簧（+） | 3.3V         |
| 磁簧（-） | GND          |
| 磁簧（S） | PIN4(GPIO31) |

![](../../media/mini2.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class MiniMagneticController(object):
    """迷你磁簧传感器控制类，磁场检测 + 输出联动控制。

    典型用法:
        ctrl = MiniMagneticController(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30)
        ctrl.set_callback(lambda t: print("触发!" if t else "释放"))
        ctrl.monitor()

    Args:
        sensor_pin:         传感器输入 GPIO，默认 GPIO31
        output_pin:         联动输出 GPIO，默认 GPIO30，传 None 禁用
        trigger_level:      触发电平，0=低电平触发，1=高电平触发，默认 0
        output_active_level: 输出激活电平，默认 1（高电平激活）
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30,
                 trigger_level=0, output_active_level=1):
        self._sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PU)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._output_active = output_active_level
        self._output_inactive = 0 if output_active_level else 1
        self._last_state = self._sensor.read()
        self._callback = None
        self._trigger_count = 0

    def set_callback(self, callback):
        """设置状态变化回调。

        Args:
            callback: 回调函数，签名 callback(is_triggered)
        """
        self._callback = callback

    def read_sensor(self):
        """读取传感器当前电平状态。"""
        return self._sensor.read()

    def is_triggered(self):
        """判断当前是否处于触发状态。"""
        return self.read_sensor() == self._trigger_level

    def set_output(self, active):
        """控制联动输出引脚电平。"""
        if self._output is not None:
            level = self._output_active if active else self._output_inactive
            self._output.write(level)

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    def wait_for_trigger(self, timeout_ms=None):
        """阻塞等待磁场触发。

        Args:
            timeout_ms: 超时 ms，None 无限等待

        Returns:
            bool: True=触发, False=超时
        """
        start = utime.ticks_ms()
        while True:
            changed, triggered = self._check_state()
            if changed and triggered:
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    def _check_state(self):
        """检测状态变化，更新输出联动和计数。"""
        state = self.read_sensor()
        triggered = state == self._trigger_level
        self.set_output(triggered)
        changed = state != self._last_state
        if changed and triggered:
            self._trigger_count += 1
            if self._callback:
                self._callback(True)
        elif changed and not triggered:
            if self._callback:
                self._callback(False)
        self._last_state = state
        return changed, triggered

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测磁场状态并联动输出。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1s
        """
        while True:
            changed, triggered = self._check_state()
            if changed:
                if triggered:
                    print("[MiniMagnetic] 触发事件")
                else:
                    print("[MiniMagnetic] 释放事件")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    controller = MiniMagneticController(
        sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30,
        trigger_level=0, output_active_level=1,
    )
    controller.monitor()
```
