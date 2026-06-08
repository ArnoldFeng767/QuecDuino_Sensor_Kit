# LED模块

## **一、** **模块介绍**

三色 RGBLED 是**全彩发光二极管模块**，由红、绿、蓝三颗芯片封装在一起，可通过 PWM 调节亮度混合出任意颜色，广泛用于氛围灯、状态指示、交互提示、创客 DIY 场景；它能实现七彩渐变、呼吸、闪烁等效果，具备体积小、亮度高、3.3V/5V 兼容、驱动简单、寿命长等优点。

**发光原理：** 

LED引脚共地，当正负极形成电压差时，LED点亮，所以高电平LED亮灯。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设     | 开发板         |
| -------- | -------------- |
| LED（-） | GND            |
| LED（R） | PIN4（GPIO31） |
| LED（G） | PIN5（GPIO30） |
| LED（B） | PIN6（GPIO32） |

![](../../media/led4.png)

## 三、 驱动代码

```python
from machine import Pin
import utime


class RGBLED(object):
    """RGB LED 控制类，通过三个 GPIO 引脚控制红、绿、蓝三色混光。

    注意：本模块为共阳极接法，电平逻辑为反逻辑 —— 0 表示点亮，1 表示熄灭。
    """

    def __init__(self, red_pin, green_pin, blue_pin):
        """初始化 RGB LED 实例。

        Args:
            red_pin: 红色通道 GPIO 引脚（Pin 对象）
            green_pin: 绿色通道 GPIO 引脚（Pin 对象）
            blue_pin: 蓝色通道 GPIO 引脚（Pin 对象）
        """
        self.red = red_pin
        self.green = green_pin
        self.blue = blue_pin

    def set_color(self, r, g, b):
        """直接设置 RGB 三通道电平。

        注意：共阳极反逻辑，0 = 点亮，1 = 熄灭。

        Args:
            r: 红色通道电平（0 或 1）
            g: 绿色通道电平（0 或 1）
            b: 蓝色通道电平（0 或 1）
        """
        self.red.write(r)
        self.green.write(g)
        self.blue.write(b)

    def set_color_by_name(self, name):
        """通过颜色名称设置 LED 颜色。

        支持的颜色：red, green, blue, yellow, purple, cyan, white, off
        """
        # 共阳极反逻辑：0 = 点亮，1 = 熄灭
        color_map = {
            "red":    (0, 1, 1),  # 仅红亮
            "green":  (1, 0, 1),  # 仅绿亮
            "blue":   (1, 1, 0),  # 仅蓝亮
            "yellow": (0, 0, 1),  # 红 + 绿
            "purple": (0, 1, 0),  # 红 + 蓝
            "cyan":   (1, 0, 0),  # 绿 + 蓝
            "white":  (0, 0, 0),  # 红 + 绿 + 蓝（全亮）
            "off":    (1, 1, 1),  # 全部熄灭
        }
        if name in color_map:
            self.set_color(*color_map[name])


if __name__ == "__main__":
    # 引脚映射：R -> GPIO32, G -> GPIO30, B -> GPIO31
    rgb_led = RGBLED(
        red_pin=Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0),
        green_pin=Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0),
        blue_pin=Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 0),
    )

    # 循环展示所有预设颜色
    colors = ["red", "green", "blue", "yellow", "purple", "cyan", "white", "off"]
    while True:
        for color in colors:
            rgb_led.set_color_by_name(color)
            print("LED color set to {}".format(color))
            utime.sleep(1)
```

