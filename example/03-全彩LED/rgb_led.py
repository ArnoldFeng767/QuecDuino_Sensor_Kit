from machine import Pin
import utime

R_PIN = 32
G_PIN = 30
B_PIN = 31

r = Pin(Pin.GPIO32, Pin.OUT,Pin.PULL_DISABLE, 0)
g = Pin(Pin.GPIO30, Pin.OUT,Pin.PULL_DISABLE, 0)
b = Pin(Pin.GPIO31, Pin.OUT,Pin.PULL_DISABLE, 0)

def set_color(red, green, blue):
    r.write(red)
    g.write(green)
    b.write(blue)
#排列组合展示多种灯色
while True:
    set_color(1, 0, 0)  # 红色
    utime.sleep(1)
    set_color(0, 1, 0)  # 绿色
    utime.sleep(1)
    set_color(0, 0, 1)  # 蓝色
    utime.sleep(1)
    set_color(1, 1, 0)  # 黄色
    utime.sleep(1)
    set_color(1, 0, 1)  # 紫色
    utime.sleep(1)  
    set_color(0, 1, 1)  # 青色
    utime.sleep(1)
    set_color(1, 1, 1)  # 白色
    utime.sleep(1)


