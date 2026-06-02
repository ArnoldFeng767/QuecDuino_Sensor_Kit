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
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def set_color(self, red, green, blue):
        self.red.write(red)
        self.green.write(green)
        self.blue.write(blue)

    def set_color_by_name(self, name):
        color_map = {
            "red": (0, 1, 1),
            "green": (1, 0, 1),
            "blue": (1, 1, 0),
            "yellow": (0, 0, 1),
            "purple": (0, 1, 0),
            "cyan": (1, 0, 0),
            "white": (0, 0, 0),
            "off": (1, 1, 1)
        }
        if name in color_map:
            self.set_color(*color_map[name])

if __name__ == "__main__":
    # Modify according to the actual pins of your development board, such as Pin.GPIO31, Pin.GPIO30, and Pin.GPIO29
    rgb_led = RGBLED(
        red=Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 0),
        green=Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 0),
        blue=Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 0)
    )

    colors = ["red", "green", "blue", "yellow", "purple", "cyan", "white", "off"]
    while True:
        for color in colors:
            rgb_led.set_color_by_name(color)
            print("LED color set to {}".format(color))
            utime.sleep(1)
```

