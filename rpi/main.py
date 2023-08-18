#!/usr/bin/env python

import time
import threading
import modules.serial_handler as serial_handler
import modules.health_handler as health_handler
import modules.instructions_handler as instructions_handler
import modules.sensors_handler as sensors_handler

Serial = serial_handler.SerialHandler().Serial

InstructionsHandler = instructions_handler.InstructionsHandler()

SensorsHandler = sensors_handler.SensorsHandler()

HealthHandler = health_handler.HealthHandler()


def handle_stage():
    pass


def check_health():
    pass


def read():
    while InstructionsHandler.stage != False:
        SensorsHandler.parse_sensors_line(line=Serial.readLine())
        HealthHandler.update_health_log(sensors=SensorsHandler.sensors)
        time.sleep(0.05)


def process():
    while InstructionsHandler.stage != False:
        InstructionsHandler.update_instructions(sensors=SensorsHandler.sensors)
        time.sleep(0.05)


def write():
    while HealthHandler.launch_health == False:
        pass

    while InstructionsHandler.stage != False:
        Serial.write(InstructionsHandler.instructions_line.encode())
        time.sleep(0.1)


if __name__ == "__main__":
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
