#!/usr/bin/env python

import math


def parse_sensors_line(line, test_mode):
    if not test_mode:
        line.decode("UTF-16", errors='ignore')
        cleaned_bytes = line.replace(b'\r', b'').replace(b'\n', b'')
        line = cleaned_bytes.decode()
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
    try:
        for sensor in line.split(" "):
            sensors = stringToDictValue(sensor, sensors)
        sensors = calculate_pitch_roll(sensors)
    except:
        pass
    return sensors


def stringToDictValue(sensor, sensors):
    key = sensor[:2]
    value = sensor[2:]
    sensors[key] = int(value)
    return sensors


def calculate_pitch_roll(sensors):
    pitch = -(math.atan2(sensors["ax"], math.sqrt(sensors["ay"] *
                                                  sensors["ay"] + sensors["az"]*sensors["az"]))*180.0)/math.pi
    roll = (math.atan2(sensors["ay"], sensors["az"])*180.0)/math.pi
    sensors["pt"] = pitch
    sensors["rl"] = roll
    return sensors
