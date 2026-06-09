"""
@file      : obstacle_avoidance.py
@author    : Aaron Chen
@brief     : KY-032 infrared obstacle avoidance sensor driver
@version   : 0.2
@date      : 2026-04-10
@copyright : Copyright (c) 2026
"""

from machine import Pin, ExtInt
import utime


class ObstacleSensor(object):
    """红外避障传感器类（KY-032），支持轮询和中断两种检测模式。

    传感器输出逻辑：
        - 无障碍物时 OUT 输出高电平 (1)
        - 检测到障碍物时 OUT 输出低电平 (0)

    应用场景：智能小车避障、自动门感应、限位检测、智能垃圾桶等。

    KY-032 引脚说明：
        VCC: 3.3-5V
        GND: 接地
        OUT: 数字输出（低电平 = 有障碍物）
        EN:  使能引脚（可选，悬空默认使能）
    注意：模块上有两个电位器可调节检测距离和灵敏度。
    """

    def __init__(self, pin=Pin.GPIO31, pull=Pin.PULL_PU):
        """初始化避障传感器实例。

        Args:
            pin: GPIO 引脚号，默认 GPIO31
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.obstacle_flag = False
        self._extint = None

    def read_state(self):
        """读取当前传感器状态。

        Returns:
            int: 0 表示检测到障碍物，1 表示无障碍物
        """
        return self.gpio.read()

    def is_obstacle(self):
        """判断当前是否有障碍物。

        Returns:
            bool: True 表示检测到障碍物
        """
        return self.read_state() == 0

    def _irq_handler(self, args):
        """中断回调函数，检测到障碍物时置位标志。

        Args:
            args: 中断事件参数，由底层传入
        """
        if self.gpio.read() == 0:
            self.obstacle_flag = True

    def monitor_polling(self, interval_ms=200):
        """轮询模式：循环读取传感器状态。

        适用于对实时性要求不高的场景，如限位检测、定期巡检。

        Args:
            interval_ms: 轮询间隔，单位毫秒，默认 200ms
        """
        print("[ObstacleSensor] 轮询模式启动")
        while True:
            if self.is_obstacle():
                print("检测到障碍物")
            else:
                print("无障碍物")
            utime.sleep_ms(interval_ms)

    def monitor_interrupt(self, interval_ms=200):
        """中断模式：障碍物出现时触发中断，主循环检查标志位。

        适用于需要快速响应的场景，如智能小车避障。

        Args:
            interval_ms: 主循环检查间隔，单位毫秒，默认 200ms
        """
        self._extint = ExtInt(self.gpio, ExtInt.IRQ_FALLING, Pin.PULL_PU, self._irq_handler)
        self._extint.enable()
        print("[ObstacleSensor] 中断模式启动")
        while True:
            if self.obstacle_flag:
                print("检测到障碍物")
                self.obstacle_flag = False
            else:
                print("无障碍物")
            utime.sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = ObstacleSensor(pin=Pin.GPIO31)

    # 轮询模式
    sensor.monitor_polling(interval_ms=200)

    # 中断模式（取消注释以切换）
    # sensor.monitor_interrupt(interval_ms=200)
