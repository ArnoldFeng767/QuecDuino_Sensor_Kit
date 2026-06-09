"""
@file      : gpio.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based magnetic reed switch detection using GPIO polling
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class ReedSwitch(object):
    """磁簧开关传感器类（GPIO 模式），通过数字量检测磁场状态变化。

    应用场景：门窗防盗报警、液位浮子开关、设备到位检测、无触点开关等。
    常见接线为上拉输入，磁铁靠近时输出低电平（触发）。
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        """初始化磁簧开关传感器实例（GPIO 模式）。

        Args:
            pin: GPIO 引脚号，默认 GPIO31
            trigger_level: 触发电平，0 = 低电平触发，1 = 高电平触发，默认 0
            pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        """
        self.gpio = Pin(pin, Pin.IN, pull)
        self.trigger_level = trigger_level
        self.last_state = self.gpio.read()

    def read_state(self):
        """读取当前 GPIO 电平状态。

        Returns:
            int: 0 或 1
        """
        return self.gpio.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到磁场）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_state() == self.trigger_level

    def check_state_change(self):
        """检测状态是否发生变化，并更新记录。

        实际应用场景：门磁防盗——开门触发报警，关门恢复正常。
        状态变化表示磁场发生了改变（如门窗被打开或关闭）。

        Returns:
            tuple: (是否变化, 当前状态)
        """
        current = self.read_state()
        changed = current != self.last_state
        self.last_state = current
        return changed, current

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测并输出磁场状态变化。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1 秒
        """
        while True:
            changed, state = self.check_state_change()

            if changed:
                if state == self.trigger_level:
                    print("[ReedSwitch] 触发：检测到磁场变化")
                else:
                    print("[ReedSwitch] 释放：磁场恢复正常")
            else:
                print("[ReedSwitch] 稳定：状态未变化")

            utime.sleep(interval_sec)


if __name__ == "__main__":
    # 默认上拉输入，低电平触发
    sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    sensor.monitor(interval_sec=1)