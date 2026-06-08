# 按键模块

## **一、** **模块介绍**

按键模块是**最基础的数字输入模块**，通过轻触开关实现通断控制，输出高低电平信号，用于实现**人机交互、开关控制、触发指令、计数、模式切换**等功能，是嵌入式 / 物联网项目必备模块。

**1、核心参数**

- 类型：轻触按键（机械式）
- 供电：3.3V–5V
- 输出：**数字信号（高 / 低电平）**
- 引脚：3 针（VCC、GND、SIG）
- 默认状态：**高电平（未按下）**
- 触发状态：**低电平（按下）**
- 自带：上拉电阻、信号指示灯

**2、原理图**

![](../../media/key1.png)

vcc和电阻都在芯片内部，当按键断开时，流过电阻的电流称为灌电流，大概几十毫安，因此此时引脚为高电平。按下时与地接通为低电平

## **二、** **连接示例**

根据表格和图片指导，将外设与开发板一一对应连接

| **外设**     | **模块**     |
| ------------ | ------------ |
| **KEY（+）** | 3.3V         |
| **KEY（-）** | GND          |
| **KEY（S）** | PIN4(GPIO31) |

![](../../media/key2.png)

## **三、** **驱动代码**

```python
import utime
from machine import ExtInt, Pin


class KeyInterrupt(object):

    def __init__(self, pin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_PU, filter_time=50, user_callback=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        self.filter_time = filter_time
        self.user_callback = user_callback
        self.press_count = 0
        # 注册外部中断，按键按下时触发 _irq_handler
        self._extint = ExtInt(self.pin, self.mode, self.pull, self._irq_handler, self.filter_time)

    def _irq_handler(self, args):
        self.press_count += 1
        print("[KeyInterrupt] key pressed, count = {}".format(self.press_count))
        if self.user_callback:
            self.user_callback(args, self.press_count)

    def enable(self):
        self._extint.enable()

    def disable(self):
        self._extint.disable()

    def reset_count(self):
        self.press_count = 0


def on_key_pressed(args, count):
    print("[UserCallback] args = {}, count = {}".format(args, count))


if __name__ == "__main__":
    # 根据开发板实际引脚修改，此处使用 GPIO31
    key = KeyInterrupt(
        pin=Pin.GPIO31,
        mode=ExtInt.IRQ_FALLING,
        pull=Pin.PULL_PU,
        filter_time=50,
        user_callback=on_key_pressed,
    )
    key.enable()

    print("Key interrupt is enabled. Press the key to trigger interrupt.")
    # 保持主线程运行，等待中断触发
    while True:
        utime.sleep_ms(500)
```

 