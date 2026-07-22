"""
@file      : key_ExtInt.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : Class-based key interrupt example for QuecPython
@version   : 0.2
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

import utime
from machine import ExtInt, Pin


class KeyInterrupt(object):
    """按键中断驱动类，基于外部中断实现按键检测、轮询与计数。

    支持两种使用模式：
        - 中断模式：注册回调，按键按下自动触发
        - 轮询模式：主动调用 read_state() / is_pressed()

    典型用法:
        # 中断模式
        key = KeyInterrupt(Pin.GPIO31)
        key.set_callback(lambda args, cnt: print("pressed", cnt))
        key.enable()

        # 轮询模式
        while True:
            if key.is_pressed():
                print("key down")
            utime.sleep_ms(100)

    Args:
        pin:         GPIO 引脚号，例如 Pin.GPIO31
        mode:        中断触发模式，默认下降沿 (ExtInt.IRQ_FALLING)
        pull:        上下拉配置，默认上拉 (Pin.PULL_PU)
        filter_time: 硬件消抖时间，单位 ms，默认 50
        callback:    用户回调函数，签名 callback(args, count)
    """

    def __init__(self, pin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_PU,
                 filter_time=50, callback=None):
        self._pin_obj = Pin(pin, Pin.IN, pull)
        self._press_count = 0
        self._callback = callback
        self._extint = ExtInt(pin, mode, pull, self._irq_handler, filter_time)

    # ---- 中断回调 ----

    def _irq_handler(self, args):
        """中断服务函数，在中断上下文中执行，不宜做耗时操作。

        Args:
            args: 中断事件参数，由底层传入
        """
        self._press_count += 1
        if self._callback:
            self._callback(args, self._press_count)

    # ---- 回调管理 ----

    def set_callback(self, callback):
        """设置或替换用户回调函数。

        Args:
            callback: 回调函数，签名 callback(args, count)，传 None 取消回调
        """
        self._callback = callback

    # ---- 中断控制 ----

    def enable(self):
        """使能按键中断。"""
        self._extint.enable()

    def disable(self):
        """禁用按键中断。"""
        self._extint.disable()

    # ---- 轮询读取 ----

    def read_state(self):
        """读取按键当前 GPIO 电平。

        Returns:
            int: 0=按下, 1=释放
        """
        return self._pin_obj.read()

    def is_pressed(self):
        """判断按键当前是否被按下。

        Returns:
            bool: True 表示按下
        """
        return self.read_state() == 0

    # ---- 计数 ----

    @property
    def count(self):
        """获取累计按下次数。"""
        return self._press_count

    def reset_count(self):
        """重置按键计数归零。"""
        self._press_count = 0

    # ---- 阻塞等待 ----

    def wait_for_press(self, timeout_ms=None):
        """阻塞等待按键按下，可选超时。

        Args:
            timeout_ms: 超时时间（ms），None 表示无限等待

        Returns:
            bool: True 表示按下，False 表示超时
        """
        start = utime.ticks_ms()
        while True:
            if self.is_pressed():
                return True
            if timeout_ms is not None:
                if utime.ticks_diff(utime.ticks_ms(), start) >= timeout_ms:
                    return False
            utime.sleep_ms(10)


def on_key_pressed(args, count):
    """示例回调函数，按键按下时打印中断参数和计数。"""
    print("[Callback] pressed, count = {}".format(count))


# ---- 独立运行测试 ----
if __name__ == "__main__":
    key = KeyInterrupt(
        pin=Pin.GPIO31,
        mode=ExtInt.IRQ_FALLING,
        pull=Pin.PULL_PU,
        filter_time=50,
        callback=on_key_pressed,
    )
    key.enable()
    print("按键中断已启用，按下按键触发。")

    while True:
        utime.sleep_ms(500)
