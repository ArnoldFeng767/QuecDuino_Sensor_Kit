# 数码管模块

## **一、** **模块介绍**

单位数码管模块是**数字显示器件**，由 7 段发光二极管组成，用于显示 0-9 数字及简单符号，广泛用于计数、计时、状态显示、创客 DIY 场景；它亮度高、显示清晰、3.3V/5V 兼容、驱动简单、使用寿命长。

**LED组成：**

7 段 LED 发光段、公共端、小数点、限流电阻、PCB 板、接线端子

**发光原理：**

模块有正极、负极、段选信号端。通过控制不同段的亮灭，组合显示 0-9 数字，开发板通过 GPIO 输出电平控制对应段点亮。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设     | 开发板 |
| -------- | ------ |
| LED（+） | 3.3V   |
| LED（-） | GND    |
| LED（S） | 自选   |

 

![](../media/display1.png)

## 三、 操作步骤

请参考目录中的开发指导手册

![](../media/test1.png)

## 四、 驱动代码

```
/# 初始化数码管各段 GPIO

seg32 = Pin(Pin.GPIO32, Pin.OUT, Pin.PULL_DISABLE, 1)  # 右下 a

seg31 = Pin(Pin.GPIO31, Pin.OUT, Pin.PULL_DISABLE, 1)  # 正上 b

seg30 = Pin(Pin.GPIO30, Pin.OUT, Pin.PULL_DISABLE, 1)  # 右上 c

seg33 = Pin(Pin.GPIO33, Pin.OUT, Pin.PULL_DISABLE, 1)  # 正下 d

seg2 = Pin(Pin.GPIO2,  Pin.OUT, Pin.PULL_DISABLE, 1)  # 中间 e

seg3 = Pin(Pin.GPIO3,  Pin.OUT, Pin.PULL_DISABLE, 1)  # 小数点 f

seg14 = Pin(Pin.GPIO14, Pin.OUT, Pin.PULL_DISABLE, 1)  # 左下 g

seg15 = Pin(Pin.GPIO15, Pin.OUT, Pin.PULL_DISABLE, 1)  # 左上 h

/# 段码表：0~9 对应各段亮灭（0亮1灭）

/# 顺序：a b c d e f g h

num_table = [

  [0,0,0,0,1,0,0,0],  # 0

  [0,1,0,1,1,0,1,1],  # 1

  [1,0,0,0,0,0,0,1],  # 2

  [0,0,0,0,0,0,1,1],  # 3

  [0,1,0,1,0,0,1,0],  # 4

  [0,0,1,0,0,0,1,0],  # 5

  [0,0,1,0,0,0,0,0],  # 6

  [0,0,0,1,1,0,1,1],  # 7

  [0,0,0,0,0,0,0,0],  # 8

  [0,0,0,0,0,0,1,0],  # 9

]

 

def display_num(n):

  if n < 0 or n > 9:

​    return

  val = num_table[n]

  seg32.write(val[0])

  seg31.write(val[1])

  seg30.write(val[2])

  seg33.write(val[3])

  seg2.write(val[4])

  seg3.write(val[5])

  seg14.write(val[6])

  seg15.write(val[7])

 

/# 循环显示 0-9

while True:

  for i in range(10):

​    display_num(i)

​    utime.sleep(1)

 
```

