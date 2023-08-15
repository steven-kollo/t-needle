#!/usr/bin/env python

#THROTTLE = "T"
#ROLL = "R"
#PITCH = "P"
#YAW = "Y"
#FLIGHT_MODE = "F"

import threading
import time
import system_check
import process_sensors
import yaw_correction
import serial_test_object

test_mode = True

global SENSORS
SENSORS = {
    "he": 0,
    "ax": 0,
    "ay": 0,
    "az": 0,
    "mx": 0,
    "my": 0,
    "mz": 0,
    "pt": 0,
    "rl": 0
}

global STAGES
STAGES = [[5, 0], [5, 90], [5, 180], [5, 90]]

global STAGE
STAGE = {
    "time": STAGES[0][0],
    "yaw": STAGES[0][1]
}

global CLOCK
CLOCK = time.time()

global YAW_CORRECTION
YAW_CORRECTION = 0

global SERIAL
if (test_mode):
    SERIAL = serial_test_object.create_serial_test_object()
else:
    import serial
    SERIAL = serial.Serial(
        port="/dev/ttyAMA0",
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0.1,
    )


def next_stage():
    global STAGES
    global CLOCK
    global STAGE
    CLOCK = CLOCK + STAGE["time"]
    STAGES.pop(0)
    if (len(STAGES) > 0):
        STAGE = {
            "time": STAGES[0][0],
            "yaw": STAGES[0][1]
        }
    else:
        STAGE = False


def read():
    while len(STAGES) > 0:
        global SENSORS
        global SERIAL
        line = SERIAL.readLine()
        SENSORS = process_sensors.parse_sensors_line(
            line=line, test_mode=test_mode)
        time.sleep(0.05)


def process():
    global STAGE
    global STAGES
    global YAW_CORRECTION
    global CLOCK
    global SENSORS

    while len(STAGES) > 0:
        DIFF = - (CLOCK - time.time())
        YAW_CORRECTION = yaw_correction.get_yaw_diff_degrees(
            yaw_current=SENSORS["he"], yaw_target=STAGE["yaw"])
        if (DIFF > STAGE["time"]):
            next_stage()
        time.sleep(0.05)


def write():
    global SERIAL
    TEMP_CORRECTION = YAW_CORRECTION
    while len(STAGES) > 0:
        print(TEMP_CORRECTION)
        if (TEMP_CORRECTION != YAW_CORRECTION):
            TEMP_CORRECTION = YAW_CORRECTION
            SERIAL.write("INSTRUCTIONS".encode())
        time.sleep(0.1)


if __name__ == "__main__":
    if system_check.system_check_on_launch(serial=SERIAL, test_mode=test_mode, try_num=1) == True:
        print(f"======= SYSTEM CHECK OK =======")
        time.sleep(3)

        r_thread = threading.Thread(target=read)
        p_thread2 = threading.Thread(target=process)
        w_thread3 = threading.Thread(target=write)

        r_thread.start()
        p_thread2.start()
        w_thread3.start()

        r_thread.join()
        p_thread2.join()
        w_thread3.join()

        print("====== ALL STAGES ENDED =======")
    else:
        print("======== LAUNCH FAILED ========")
