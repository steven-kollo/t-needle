# yaw_target = yaw_current + correction, yaw is calculated in degrees
def get_yaw_diff_degrees(yaw_current, yaw_target):
    plus_c = yaw_target + 360 - yaw_current
    plus = yaw_target - yaw_current
    minus_c = yaw_current - yaw_target + 360
    minus = yaw_current - yaw_target

    if (plus >= 0 and plus <= 180):
        return plus
    if (plus_c >= 0 and plus_c <= 180):
        return plus_c
    if (minus >= 0 and minus <= 180):
        return -minus
    if (minus_c >= 0 and minus_c <= 180):
        return -minus_c
