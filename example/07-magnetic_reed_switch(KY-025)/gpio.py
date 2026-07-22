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

    典型用法:
        sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
        sensor.set_callback(lambda state: print("触发!" if state else "释放"))
        sensor.monitor(interval_sec=1)

    Args:
        pin:           GPIO 引脚号，默认 GPIO31
        trigger_level: 触发电平，0=低电平触发，1=高电平触发，默认 0
        pull:          上下拉配置，默认上拉 (Pin.PULL_PU)
    """

    def __init__(self, pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU):
        self._gpio = Pin(pin, Pin.IN, pull)
        self._trigger_level = trigger_level
        self._last_state = self._gpio.read()
        self._callback = None
        self._trigger_count = 0

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置状态变化回调。

        Args:
            callback: 回调函数，签名 callback(is_triggered)
        """
        self._callback = callback

    # ---- 读取 ----

    def read_state(self):
        """读取当前 GPIO 电平状态。

        Returns:
            int: 0 或 1
        """
        return self._gpio.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到磁场）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_state() == self._trigger_level

    # ---- 状态变化 ----

    def check_state_change(self):
        """检测状态是否发生变化，并更新记录。

        Returns:
            tuple: (是否变化, 当前电平)
        """
        current = self.read_state()
        changed = current != self._last_state
        if changed:
            if current == self._trigger_level:
                self._trigger_count += 1
            if self._callback:
                self._callback(current == self._trigger_level)
        self._last_state = current
        return changed, current

    # ---- 计数 ----

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    # ---- 阻塞等待 ----

    def wait_for_trigger(self, timeout_ms=None):
        """阻塞等待磁场触发，可选超时。

        Args:
            timeout_ms: 超时时间 ms，None 无限等待

        Returns:
            bool: True=触发, False=超时
        """
        start = utime.ticks_ms()
        while True:
            changed, state = self.check_state_change()
            if changed and state == self._trigger_level:
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    # ---- 监控 ----

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测并输出磁场状态变化。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1s
        """
        while True:
            changed, state = self.check_state_change()
            if changed:
                if state == self._trigger_level:
                    print("[ReedSwitch] 触发：检测到磁场变化")
                else:
                    print("[ReedSwitch] 释放：磁场恢复正常")
            utime.sleep(interval_sec)


# ---- 独立运行测试 ----
if __name__ == "__main__":
    sensor = ReedSwitch(pin=Pin.GPIO31, trigger_level=0, pull=Pin.PULL_PU)
    sensor.monitor(interval_sec=1)
