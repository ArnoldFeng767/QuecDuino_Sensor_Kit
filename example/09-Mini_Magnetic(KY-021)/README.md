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

    应用场景：门磁触发后联动输出，驱动告警灯、蜂鸣器或继电器。
    """

    def __init__(
        self,
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    ):
        """初始化磁簧传感器控制器。

        Args:
            sensor_pin: 传感器输入 GPIO 引脚号，默认 GPIO31
            output_pin: 联动输出 GPIO 引脚号，默认 GPIO30
            trigger_level: 触发电平，0 = 低电平触发，1 = 高电平触发，默认 0
            output_active_level: 输出激活电平，默认 1（高电平激活）
        """
        self.sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PU)
        self.output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level
        self.output_active_level = output_active_level
        self.output_inactive_level = 0 if output_active_level else 1
        self.last_state = self.sensor.read()

    def read_sensor(self):
        """读取传感器当前电平状态。"""
        return self.sensor.read()

    def is_triggered(self):
        """判断当前是否处于触发状态。"""
        return self.read_sensor() == self.trigger_level

    def set_output(self, active):
        """控制联动输出引脚电平，可用于驱动 LED、蜂鸣器、继电器等。"""
        level = self.output_active_level if active else self.output_inactive_level
        self.output.write(level)

    def update(self):
        """根据传感器状态更新联动输出，并返回状态变化信息。"""
        state = self.read_sensor()
        triggered = state == self.trigger_level
        self.set_output(triggered)

        if triggered:
            print("检测到磁场变化")
        else:
            print("未检测到磁场变化")

        changed = state != self.last_state
        self.last_state = state
        return changed, triggered

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测磁场状态并联动输出。

        实际应用场景：门禁状态指示和入侵检测等。
        """
        while True:
            changed, triggered = self.update()
            if changed:
                if triggered:
                    print("[MiniMagnetic] 触发事件")
                else:
                    print("[MiniMagnetic] 释放事件")
            utime.sleep(interval_sec)


if __name__ == '__main__':
    controller = MiniMagneticController(
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    )
    controller.monitor()
```
