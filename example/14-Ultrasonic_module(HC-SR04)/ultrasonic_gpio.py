from machine import Pin
import utime

# Pin definition (modified according to actual wiring)
TRIG_PIN = Pin.GPIO30  # Trigger pin
ECHO_PIN = Pin.GPIO31  # Echo pin

TRIG = Pin(TRIG_PIN, Pin.OUT, Pin.PULL_DISABLE, 0)
ECHO = Pin(ECHO_PIN, Pin.IN, Pin.PULL_DISABLE, 0)

# Simple moving average filter, taking the average of multiple measurements
dist_list = []
FILTER_SIZE = 5  # Filter window size

def rcwl_9610a_get_dist():
    TRIG.off()
    utime.sleep_us(2)
    TRIG.on()
    utime.sleep_us(10)
    TRIG.off()

    # Optimize timeout to avoid false positives
    t_out = 0
    while ECHO.value() == 0 and t_out < 30000:
        t_out += 1
    if t_out >= 30000:
        return None

    start = utime.ticks_us()

    t_out = 0
    while ECHO.value() == 1 and t_out < 500000:  # Maximum range 8m, corresponding to about 480000us
        t_out += 1
    if t_out >= 500000:
        return None

    end = utime.ticks_us()
    dura = end - start
    dist = dura / 58.0
    return round(dist, 2)

while True:
    raw_dist = rcwl_9610a_get_dist()
    
    if raw_dist is not None and 2 <= raw_dist <= 800:
        # Simple moving average filter
        dist_list.append(raw_dist)
        if len(dist_list) > FILTER_SIZE:
            dist_list.pop(0)
        avg_dist = round(sum(dist_list) / len(dist_list), 2)
        print("Current distance:", avg_dist, "cm")
    else:
        print("Out of range or signal error")

    utime.sleep(0.2)





