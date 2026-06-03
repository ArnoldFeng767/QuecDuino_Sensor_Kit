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
rom machine import Pin
import utime


class InclinationSwitch:
    """Tilt switch sensor packaging class."""

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        self.gpio = Pin(pin, Pin.IN, pull)
        self.led = Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.trigger_level = trigger_level

    def read_state(self):
        return self.gpio.read()

    def is_tilted(self):
        return self.read_state() == self.trigger_level

    def monitor(self):
        while True:
            if self.is_tilted():
                self.led.write(1)
                print("Tilt detected")
            else:
                self.led.write(0)
                print("Level state")
            utime.sleep(1)

def main():
    tilt_switch = InclinationSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    tilt_switch.monitor()

if __name__ == '__main__':
    main()
```

