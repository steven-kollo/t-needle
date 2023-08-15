import time
import process_sensors
import rpi_config


def check_pitch_roll(collection):
    pitch_avg = sum(collection['pt']) / len(collection['pt'])
    roll_avg = sum(collection['rl']) / len(collection['rl'])
    error = rpi_config.system_check_on_launch["pitch_roll_error_degrees"]

    if (pitch_avg < error and pitch_avg > -error and roll_avg < error and roll_avg > -error):

        print("-------- Pitch Roll OK --------")
        print(
            f"------ Pitch: {round(pitch_avg)} Roll: {round(roll_avg)} ------\n")
        return True
    else:
        return False


def check_connection(collection):
    # MOD vs PEAKS for each sensor
    avg_error = []
    error = rpi_config.system_check_on_launch["sensor_error_percents"]
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
    print(avg_error)

    avg_error = sum(avg_error)/len(avg_error)
    print("-------- Connection OK --------")
    print(f"Avg error is {round(avg_error)}%")
    return True


def append_sensors_to_collection(sensors, collection):
    for sensor in sensors:
        collection[sensor].append(sensors[sensor])
    return collection


def create_sensor_data_collection(serial, test_mode):
    collection = rpi_config.system_check_on_launch["collection"]
    counter = 0

    while counter != rpi_config.system_check_on_launch["num_of_sensor_cycles"]:
        line = serial.readLine()

        sensors = process_sensors.parse_sensors_line(
            line=line, test_mode=test_mode)

        collection = append_sensors_to_collection(
            sensors, collection)

        time.sleep(
            rpi_config.system_check_on_launch["sensor_cycle_time_sleep"])

        counter += 1

    return collection


def system_check_on_launch(serial, test_mode, try_num):
    collection = create_sensor_data_collection(serial, test_mode)

    if check_pitch_roll(collection) == True and check_connection(collection) == True:
        return True

    elif try_num < rpi_config.system_check_on_launch["num_of_tries"]:
        print(f"==== {try_num} SYSTEM CHECK FAILED ====\n")
        return system_check_on_launch(serial, test_mode, try_num + 1)

    else:
        return False
