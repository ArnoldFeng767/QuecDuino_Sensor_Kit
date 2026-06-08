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
    """按键中断类，基于外部中断实现按键检测与计数。

    Args:
        pin: GPIO 引脚号，例如 Pin.GPIO31
        mode: 中断触发模式，默认下降沿触发 (ExtInt.IRQ_FALLING)
        pull: 上下拉配置，默认上拉 (Pin.PULL_PU)
        filter_time: 消抖时间，单位毫秒，默认 50ms
        user_callback: 用户自定义回调函数，签名为 callback(args, count)
    """

    def __init__(self, pin, mode=ExtInt.IRQ_FALLING, pull=Pin.PULL_PU, filter_time=50, user_callback=None):
        self.pin = pin
        self.mode = mode
        self.pull = pull
        self.filter_time = filter_time
        self.user_callback = user_callback
        self.press_count = 0
        # 注册外部中断，按键按下时触发 _irq_handler
        self._extint = ExtInt(self.pin, self.mode, self.pull, self._irq_handler, self.filter_time)

    def _irq_handler(self, args):
        """中断服务函数，在中断上下文中执行，不宜做耗时操作。

        Args:
            args: 中断事件参数，由底层传入
        """
        self.press_count += 1
        print("[KeyInterrupt] key pressed, count = {}".format(self.press_count))
        if self.user_callback:
            self.user_callback(args, self.press_count)

    def enable(self):
        """使能按键中断。"""
        self._extint.enable()

    def disable(self):
        """禁用按键中断。"""
        self._extint.disable()

    def reset_count(self):
        """重置按键计数归零。"""
        self.press_count = 0


def on_key_pressed(args, count):
    """示例回调函数，按键按下时打印中断参数和计数。"""
    print("[UserCallback] args = {}, count = {}".format(args, count))


if __name__ == "__main__":
    # 根据开发板实际引脚修改，此处使用 GPIO31
    key = KeyInterrupt(
        pin=Pin.GPIO31,
        mode=ExtInt.IRQ_FALLING,
        pull=Pin.PULL_PU,
        filter_time=50,
        user_callback=on_key_pressed,
    )
    key.enable()

    print("Key interrupt is enabled. Press the key to trigger interrupt.")
    # 保持主线程运行，等待中断触发
    while True:
        utime.sleep_ms(500)



