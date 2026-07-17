"""
@file      : flame.py
@author    : Aaron Chen
@brief     : Class-based flame sensor demo using GPIO.
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""


from machine import Pin
import utime


class FlameDigitalSensor(object):
    """火焰传感器类（GPIO 模式），通过数字量检测火焰并联动输出。

    典型用法:
        sensor = FlameDigitalSensor(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30)
        sensor.set_callback(lambda detected: print("火!" if detected else ""))
        sensor.monitor()

    Args:
        sensor_pin: 传感器输入 GPIO，默认 GPIO31
        output_pin: 联动输出 GPIO，默认 GPIO30，传 None 禁用
        trigger_level: 触发电平，1=高电平触发，0=低电平触发，默认 1
    """

    def __init__(self, sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1):
        self._sensor = Pin(sensor_pin, Pin.IN, Pin.PULL_PD)
        self._output = None
        if output_pin is not None:
            self._output = Pin(output_pin, Pin.OUT, Pin.PULL_DISABLE, 0)
        self._trigger_level = trigger_level
        self._last_state = self._sensor.read()
        self._callback = None
        self._trigger_count = 0

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置火焰检测回调。

        Args:
            callback: 回调函数，签名 callback(is_detected)
        """
        self._callback = callback

    # ---- 读取 ----

    def read_state(self):
        """读取传感器当前电平状态。

        Returns:
            int: 0 或 1
        """
        return self._sensor.read()

    def is_flame_detected(self):
        """判断当前是否检测到火焰。

        Returns:
            bool: True 表示检测到火焰
        """
        return self.read_state() == self._trigger_level

    # ---- 输出 ----

    def set_output(self, active):
        """控制联动输出引脚。

        Args:
            active: True 激活，False 关闭
        """
        if self._output is not None:
            self._output.write(1 if active else 0)

    # ---- 计数 ----

    @property
    def trigger_count(self):
        """获取累计触发次数。"""
        return self._trigger_count

    def reset_count(self):
        """重置触发计数归零。"""
        self._trigger_count = 0

    # ---- 状态检测 ----

    def _check_state(self):
        """检测状态变化，更新联动输出。"""
        state = self.read_state()
        detected = state == self._trigger_level
        self.set_output(detected)

        changed = state != self._last_state
        if changed and detected:
            self._trigger_count += 1
            if self._callback:
                self._callback(True)
        elif changed and not detected:
            if self._callback:
                self._callback(False)

        self._last_state = state
        return changed, detected

    # ---- 监控 ----

    def monitor(self, interval_ms=100):
        """轮询监控循环。

        Args:
            interval_ms: 轮询间隔 ms，默认 100
        """
        while True:
            changed, detected = self._check_state()
            if changed:
                if detected:
                    print("检测到火焰")
                else:
                    print("火焰消失")
            utime.sleep_ms(interval_ms)


if __name__ == "__main__":
    sensor = FlameDigitalSensor(sensor_pin=Pin.GPIO31, output_pin=Pin.GPIO30, trigger_level=1)
    sensor.monitor()
