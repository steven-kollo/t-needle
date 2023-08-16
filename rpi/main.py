#!/usr/bin/env python

#THROTTLE = "T"
#ROLL = "R"
#PITCH = "P"
#YAW = "Y"
#FLIGHT_MODE = "F"

import rpi_config
import threading
import time
import health_check
import handlers.sensors_handlers as sensors_handlers
import handlers.stages_handlers as stages_handlers
import handlers.instructions_handler as instructions_handler
import serial_object


test_mode = rpi_config.test_mode

global SERIAL
SERIAL = serial_object.create_serial_object(test_mode)

global sensors
sensors = rpi_config.sensors

global stages
stages = rpi_config.stages

global stage
stage = stages_handlers.push_stage(stages)

global clock
clock = time.time()

global instructions
instructions = rpi_config.instructions

global InstructionsHandler
InstructionsHandler = instructions_handler.InstructionsHandler()


def handle_stage():
    pass


def check_health():
    pass


def read():
    while stage != False:
        global sensors
        global SERIAL
        sensors = sensors_handlers.parse_sensors_line(
            line=SERIAL.readLine(), test_mode=test_mode)
        time.sleep(0.05)


def process():
    global stage
    global stages
    global clock
    global sensors
    global InstructionsHandler
    global instructions

    while stage != False:
        time_diff = - (clock - time.time())
        InstructionsHandler.update_instructions(sensors=sensors, stage=stage)
        instructions["yaw"] = InstructionsHandler.instructions["yaw"]
        if (time_diff > stage["time"]):
            next_stage = stages_handlers.next_stage(stages, stage, clock)
            stages = next_stage["stages"]
            stage = next_stage["stage"]
            clock = next_stage["clock"]
        time.sleep(0.05)


def write():
    global SERIAL
    while stage != False:
        SERIAL.write(f"{instructions['yaw']}".encode())
        time.sleep(0.1)


if __name__ == "__main__":
    if health_check.health_check_on_launch(serial=SERIAL, test_mode=test_mode, try_num=1) == True:
        time.sleep(3)

        stage_thread = threading.Thread(target=handle_stage)
        health_thread = threading.Thread(target=check_health)
        read_thread = threading.Thread(target=read)
        process_thread = threading.Thread(target=process)
        write_thread = threading.Thread(target=write)

        stage_thread.start()
        health_thread.start()
        read_thread.start()
        process_thread.start()
        write_thread.start()

        stage_thread.join()
        health_thread.join()
        read_thread.join()
        process_thread.join()
        write_thread.join()

        print("====== ALL STAGES ENDED =======")
    else:
        print("======== LAUNCH FAILED ========")
