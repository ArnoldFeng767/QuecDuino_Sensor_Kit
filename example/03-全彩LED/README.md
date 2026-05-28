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

 

![](../media/led4.png)

## 三、 操作步骤

请参考目录中的开发指导手册

![](../media/test1.png)

## 四、 驱动代码

```python
R_PIN = 32

G_PIN = 30

B_PIN = 31

 

r = Pin(Pin.GPIO32, Pin.OUT,Pin.PULL_DISABLE, 0)

g = Pin(Pin.GPIO30, Pin.OUT,Pin.PULL_DISABLE, 0)

b = Pin(Pin.GPIO31, Pin.OUT,Pin.PULL_DISABLE, 0)

 

def set_color(red, green, blue):

  r.write(red)

  g.write(green)

  b.write(blue)

/#排列组合展示多种灯色

while True:

  set_color(1, 0, 0)  # 红色

  utime.sleep(1)

  set_color(0, 1, 0)  # 绿色

  utime.sleep(1)

  set_color(0, 0, 1)  # 蓝色

  utime.sleep(1)

  set_color(1, 1, 0)  # 黄色

  utime.sleep(1)

  set_color(1, 0, 1)  # 紫色

  utime.sleep(1)  

  set_color(0, 1, 1)  # 青色

  utime.sleep(1)

  set_color(1, 1, 1)  # 白色

  utime.sleep(1)

 
```

