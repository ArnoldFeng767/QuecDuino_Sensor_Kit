"""
@file      : mini_Electromagnetics.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based mini magnetic sensor project with output linkage control.
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class MiniMagneticController(object):
    """迷你磁簧传感器控制类，磁场检测 + 输出联动控制。

    典型用法:
        ctrl = MiniMagneticController(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30)
        ctrl.set_callback(lambda triggered: print("触发!" if triggered else "释放"))
        ctrl.monitor()

    Args:
        sensor_pin:         传感器输入 GPIO，默认 GPIO31
        output_pin:         联动输出 GPIO，默认 GPIO30，传 None 禁用
        trigger_level:      触发电平，0=低电平触发，1=高电平触发，默认 0
        output_active_level: 输出激活电平，默认 1（高电平激活）
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30,
                 trigger_level=0, output_active_level=1):
        self._sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PU)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._output_active = output_active_level
        self._output_inactive = 0 if output_active_level else 1
        self._last_state = self._sensor.read()
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

    def read_sensor(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self._sensor.read()

    def is_triggered(self):
        """判断当前是否处于触发状态（检测到磁场）。

        Returns:
            bool: True 表示已触发
        """
        return self.read_sensor() == self._trigger_level

    # ---- 输出 ----

    def set_output(self, active):
        """控制联动输出引脚电平。

        Args:
            active: True 激活输出，False 关闭输出
        """
        if self._output is not None:
            level = self._output_active if active else self._output_inactive
            self._output.write(level)

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
        """阻塞等待磁场触发。

        Args:
            timeout_ms: 超时 ms，None 无限等待

        Returns:
            bool: True=触发, False=超时
        """
        start = utime.ticks_ms()
        while True:
            changed, triggered = self._check_state()
            if changed and triggered:
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)

    # ---- 内部 ----

    def _check_state(self):
        """检测状态变化，更新输出联动和计数。"""
        state = self.read_sensor()
        triggered = state == self._trigger_level
        self.set_output(triggered)

        changed = state != self._last_state
        if changed and triggered:
            self._trigger_count += 1
            if self._callback:
                self._callback(True)
        elif changed and not triggered:
            if self._callback:
                self._callback(False)

        self._last_state = state
        return changed, triggered

    # ---- 监控 ----

    def monitor(self, interval_sec=1):
        """轮询监控循环，检测磁场状态并联动输出。

        Args:
            interval_sec: 轮询间隔，单位秒，默认 1s
        """
        while True:
            changed, triggered = self._check_state()
            if changed:
                if triggered:
                    print("[MiniMagnetic] 触发事件")
                else:
                    print("[MiniMagnetic] 释放事件")
            utime.sleep(interval_sec)


# ---- 独立运行测试 ----
if __name__ == '__main__':
    controller = MiniMagneticController(
        sensor_pin=Pin.GPIO31,
        output_pin=Pin.GPIO30,
        trigger_level=0,
        output_active_level=1,
    )
    controller.monitor()
