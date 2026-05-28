# 魔术光环模块

## **一、** **模块介绍**

魔术光环模块（KY‑027）是**倾斜感应 + LED 发光**二合一数字模块，内置水银开关与高亮 LED，用于倾斜检测、姿态触发、状态指示、创客互动项目；模块体积小、响应快、数字电平输出、3.3V/5V 兼容、直接接 GPIO 驱动、寿命稳定。

**工作原理：**

![](../media/magic1.png)

模块有供电、接地、信号输出、LED 控制端。倾斜到一定角度时，水银开关导通 / 断开，输出高低电平；可通过 GPIO 控制 LED 亮灭，实现倾斜亮灯、姿态报警等效果。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设          | 开发板       |
| ------------- | ------------ |
| 魔术光环（+） | 3.3V         |
| 魔术光环（-） | GND          |
| 魔术光环（S） | PIN4(GPIO31) |
| 魔术光环（L） | PIN5(GPIO30) |

 

![](../media/magic2.png)

## 三、 操作步骤

请参考目录中的开发指导手册

![](../media/test1.png)

## 四、 驱动代码

```python
/# 配置GPIO为输入，上拉

gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)

def main():

  /# 假设传感器检测到倾斜时输出高电平（1）

  while True:

     if gpio.read() == 1:

       print("水银检测到倾斜")

       gpio1.write(1)

     else:

       print("水银没有检测到倾斜")

       gpio1.write(0)

     utime.sleep(1)

if name == 'main':

  main()
```

 