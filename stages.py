import random
import threading
import time

global STAGES
STAGES = [[5, 0], [5, 90], [5, 180], [5, 90]]

global STAGE
STAGE = {
    "time": STAGES[0][0],
    "yaw": STAGES[0][1]
}

global CLOCK
CLOCK = time.time()

global SENSOR
SENSOR = 180

global CORRECTION
CORRECTION = 0


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
        global SENSOR
        SENSOR = SENSOR + random.randint(1, 9)
        print(f"SENSOR: {SENSOR}")
        time.sleep(0.1)


def process():
    global CORRECTION
    global CLOCK
    TIME_SHIFT_MULTIPLIER = 1.3

    while len(STAGES) > 0:
        DIFF = - (CLOCK - time.time())
        CORRECTION = round((STAGE["yaw"] - SENSOR) * TIME_SHIFT_MULTIPLIER)
        if (DIFF > STAGE["time"]):
            next_stage()
        time.sleep(0.5)


def write():
    global SENSOR
    TEMP_CORRECTION = CORRECTION
    while len(STAGES) > 0:
        if (TEMP_CORRECTION != CORRECTION):
            SENSOR = SENSOR + CORRECTION
            TEMP_CORRECTION = CORRECTION
        time.sleep(0.1)


if __name__ == "__main__":
    thread1 = threading.Thread(target=read)
    thread2 = threading.Thread(target=process)
    thread3 = threading.Thread(target=write)

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    print("All stages ended")
