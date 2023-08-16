#!/usr/bin/env python

import math
import rpi_config


def append_sensors_to_collection(sensors, collection):
    for sensor in sensors:
        collection[sensor].append(sensors[sensor])
    return collection


def get_collection_mods(collection):
    # MOD vs PEAKS for each sensor
    avg_error = []
    error = rpi_config.health_check_on_launch["sensor_error_percents"]
    for single_sensor in collection:
        collection[single_sensor].sort()

        mod = collection[single_sensor][round(
            len(collection[single_sensor]) / 2)]
        highest_error = collection[single_sensor][len(
            collection[single_sensor]) - 2] / mod - 1
        lowest_error = -(collection[single_sensor][1] / mod - 1)

        avg_error.append(abs((highest_error + lowest_error) / 2 * 100))

        if (highest_error > error and highest_error > error):
            print(f"----- Connection failed {single_sensor} ----")
            return False

    avg_error = sum(avg_error)/len(avg_error)
    print("-------- Connection OK --------")
    print(f"------- Avg error is {round(avg_error)}% -------")
    return True


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
