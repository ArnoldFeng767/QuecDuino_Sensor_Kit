# 超声波模块

## **一、** **模块介绍**

HC-SR04 的工作流程由 "触发信号" 启动，通过 "回响信号" 反馈距离，具体步骤如下：

触发测距：STM32 向 Trig 引脚输出至少 10μs 的高电平信号（需高精度延时，笔者在定时器笔记中已实现，可回顾）；

模块自动发送 / 接收超声波：Trig 接收到触发信号后，模块会自动发送 8 个 40kHz 的方波，同时开始检测是否有超声波反射回来；

回响信号反馈：若超声波反射回来，模块会通过 Echo 引脚输出高电平 —— 高电平的持续时间 = 超声波从 "发射到返回" 的总时间；

距离计算：根据 "时间 - 距离" 公式推导，最终距离 = （Echo 高电平持续时间 × 声速） / 2

（注：声速取 340m/s，除以 2 是因为超声波需 "发射→反射→返回"，走了两倍距离）。

**1、核心参数**

- 工作电压：**3.3V–5V**
- 测量范围：**2cm–450cm**
- 分辨率：1mm
- 测量角度：约 15°
- 输出方式：**GPIO / I2C / UART**
- 特点：非接触、精度高、反应快、不受光线颜色影响

**2、原理图**

![](../../media/hc1.png)

**3、时序图**

![](../../media/hc2.png)



## **二、** **连接示例**

根据表格和图片指导，将外设与开发板一一对应连接

| **外设**           | **模块**     |
| ------------------ | ------------ |
| Ultrasonic（+）    | VCC(5V)      |
| Ultrasonic（Trig） | Pin5(GPIO30) |
| Ultrasonic（Echo） | Pin4(GPIO31) |
| Ultrasonic（-）    | GND          |

![](../../media/hc3.png)

## **三、** **驱动代码**

```python
from machine import Pin
import utime


class UltrasonicSensor(object):
    """超声波测距传感器类（HC-SR04），通过 Trig/Echo 引脚测量距离。

    测距原理：Trig 发送 >=10us 高电平触发，Echo 返回高电平脉冲宽度
    对应声波往返时间，距离 = 脉冲宽度(us) / 58.0（单位 cm）。

    内置滑动窗口滤波，减少单次测量误差。
    """

    def __init__(self, trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5):
        """初始化超声波传感器实例。

        Args:
            trig_pin: 触发引脚 GPIO 号，默认 GPIO30
            echo_pin: 回波引脚 GPIO 号，默认 GPIO31
            filter_size: 滑动窗口滤波大小，默认 5 次均值
        """
        self.trig = Pin(trig_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self.echo = Pin(echo_pin, Pin.IN, Pin.PULL_DISABLE, 0)
        self.filter_size = filter_size
        self.dist_list = []

    def _trigger(self):
        """发送触发信号，Trig 拉高 >=10us 后拉低。"""
        self.trig.off()
        utime.sleep_us(2)
        self.trig.on()
        utime.sleep_us(10)
        self.trig.off()

    def read_distance(self):
        """读取单次测距值，带超时保护。"""
        self._trigger()

        t_out = 0
        while self.echo.value() == 0 and t_out < 30000:
            t_out += 1
        if t_out >= 30000:
            return None

        start = utime.ticks_us()

        t_out = 0
        while self.echo.value() == 1 and t_out < 500000:
            t_out += 1
        if t_out >= 500000:
            return None

        end = utime.ticks_us()
        duration = end - start
        distance = duration / 58.0
        return round(distance, 2)

    def read_filtered_distance(self):
        """读取滤波后的距离值（滑动窗口均值）。

        有效测量范围：2cm ~ 800cm，超出范围的值被过滤。
        """
        raw_dist = self.read_distance()
        if raw_dist is None or not 2 <= raw_dist <= 800:
            return None

        self.dist_list.append(raw_dist)
        if len(self.dist_list) > self.filter_size:
            self.dist_list.pop(0)
        return round(sum(self.dist_list) / len(self.dist_list), 2)

    def monitor(self, interval_ms=200):
        """轮询监控循环，持续测量并输出距离。"""
        while True:
            avg_dist = self.read_filtered_distance()
            if avg_dist is not None:
                print("当前距离: {} cm".format(avg_dist))
            else:
                print("超出量程或信号异常")
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    ultrasonic = UltrasonicSensor(trig_pin=Pin.GPIO30, echo_pin=Pin.GPIO31, filter_size=5)
    ultrasonic.monitor(interval_ms=200)
```
