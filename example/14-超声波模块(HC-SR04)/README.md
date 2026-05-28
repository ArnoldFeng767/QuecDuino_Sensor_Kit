# 超声波模块

## **一、** **模块介绍**

HC-SR04 的工作流程由 “触发信号” 启动，通过 “回响信号” 反馈距离，具体步骤如下：

触发测距：STM32 向 Trig 引脚输出至少 10μs 的高电平信号（需高精度延时，笔者在定时器笔记中已实现，可回顾）；

模块自动发送 / 接收超声波：Trig 接收到触发信号后，模块会自动发送 8 个 40kHz 的方波，同时开始检测是否有超声波反射回来；

回响信号反馈：若超声波反射回来，模块会通过 Echo 引脚输出高电平 —— 高电平的持续时间 = 超声波从 “发射到返回” 的总时间；

距离计算：根据 “时间 - 距离” 公式推导，最终距离 = （Echo 高电平持续时间 × 声速） / 2

（注：声速取 340m/s，除以 2 是因为超声波需 “发射→反射→返回”，走了两倍距离）。

**1、核心参数**

- 工作电压：**3.3V–5V**
- 测量范围：**2cm–450cm**
- 分辨率：1mm
- 测量角度：约 15°
- 输出方式：**GPIO / I2C / UART**
- 特点：非接触、精度高、反应快、不受光线颜色影响

**2、原理图**

![](../media/hc1.png)

 

**3、时序图**

![](../media/hc2.png)

 

## **二、** **连接示例**

根据表格和图片指导，将外设与开发板一一对应连接

| **外设**           | **模块**     |
| ------------------ | ------------ |
| Ultrasonic（+）    | VCC(5V)      |
| Ultrasonic（Trig） | Pin5(GPIO30) |
| Ultrasonic（Echo） | Pin4(GPIO31) |
| Ultrasonic（-）    | GND          |

![](../media/hc3.png)

## 三、 操作步骤

请参考目录中的开发指导手册

![](../media/test1.png)

## **四、** **驱动代码**

```python
from machine import Pin

import utime

/# 引脚定义（根据实际接线修改）

TRIG_PIN = Pin.GPIO30  # 触发脚

ECHO_PIN = Pin.GPIO31  # 回声脚



/# 初始化引脚

trig = Pin(TRIG_PIN, Pin.OUT, Pin.PULL_DISABLE, 0)

echo = Pin(ECHO_PIN, Pin.IN, Pin.PULL_DISABLE, 0)

def measure_distance():

  /# 发送10us以上的高电平触发信号

  trig.write(0)

  utime.sleep_us(2)

  trig.write(1)

  utime.sleep_us(10)

  trig.write(0)



  /# 等待ECHO引脚变高（开始计时）

  timeout = utime.ticks_ms() + 200  # 超时200ms

  while echo.read() == 0:

     if utime.ticks_ms() > timeout:

       return -1  # 超时，测量失败

  start_time = utime.ticks_us()

  /# 等待ECHO引脚变低（结束计时）

  while echo.read() == 1:

     if utime.ticks_ms() > timeout:

       return -1  # 超时，测量失败



  end_time = utime.ticks_us()



  /# 计算距离（声速取340m/s，即0.034cm/us，来回除以2）

  pulse_duration = end_time - start_time

  distance = (pulse_duration * 0.034) / 2



  return round(distance, 2)



if name == "main":

  print("RCWL-9206 超声波测距模块测试（GPIO模式）")

  print("测量间隔200ms以上，避免干扰")

  while True:

     dist = measure_distance()

     if dist == -1:

       print("测量超时/失败")

     else:

       print("当前距离: {} cm".format(dist))

     utime.sleep(0.2)  # 两次测量间隔不小于200ms
```

