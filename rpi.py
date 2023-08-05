#!/usr/bin/env python

#THROTTLE = "T"
#ROLL = "R"
#PITCH = "P"
#YAW = "Y"
#FLIGHT_MODE = "F"

import serial
import time
import math


def calculate(string, sensors):
    for sensor in string.split(" "):
        sensors = stringToDictValue(sensor, sensors)

    pitch = -(math.atan2(sensors["ax"], math.sqrt(sensors["ay"] *
                                                  sensors["ay"] + sensors["az"]*sensors["az"]))*180.0)/math.pi
    roll = (math.atan2(sensors["ay"], sensors["az"])*180.0)/math.pi

    print(pitch)
    print(roll)


def stringToDictValue(sensor, sensors):
    key = sensor[:2]
    value = sensor[2:]
    sensors[key] = int(value)
    return sensors


sensors = {
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

ser = serial.Serial(
    port="/dev/ttyAMA0",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.1,
)

while True:
    ser.write("t12000 r34000 p56000 y78000 f1".encode())
    line = ser.readline()
    line.decode("UTF-16", errors='ignore')
    cleaned_bytes = line.replace(b'\r', b'').replace(b'\n', b'')
    cleaned_string = cleaned_bytes.decode()
    print(cleaned_string)
    try:
        calculate(cleaned_string, sensors)
    except:
        pass
    time.sleep(0.05)
