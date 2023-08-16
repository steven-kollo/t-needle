import time
import handlers.sensors_handlers as sensors_handlers
import rpi_config


def check_pitch_roll(collection):
    pitch_avg = sum(collection['pt']) / len(collection['pt'])
    roll_avg = sum(collection['rl']) / len(collection['rl'])
    error = rpi_config.health_check_on_launch["pitch_roll_error_degrees"]

    if (pitch_avg < error and pitch_avg > -error and roll_avg < error and roll_avg > -error):

        print("-------- Pitch Roll OK --------")
        print(
            f"------ Pitch: {round(pitch_avg)} Roll: {round(roll_avg)} ------\n")
        return True
    else:
        return False


def create_sensor_data_collection(serial, test_mode):
    collection = rpi_config.collection
    counter = 0

    while counter != rpi_config.health_check_on_launch["num_of_sensor_cycles"]:
        line = serial.readLine()

        sensors = sensors_handlers.parse_sensors_line(
            line=line, test_mode=test_mode)

        collection = sensors_handlers.append_sensors_to_collection(
            sensors, collection)

        time.sleep(
            rpi_config.health_check_on_launch["sensor_cycle_time_sleep"])

        counter += 1

    return collection


def health_check_on_launch(serial, test_mode, try_num):
    collection = create_sensor_data_collection(serial, test_mode)

    if check_pitch_roll(collection) == True and sensors_handlers.get_collection_mods(collection) == True:
        print(f"======= HEALTH CHECK OK =======")
        return True

    elif try_num < rpi_config.health_check_on_launch["num_of_tries"]:
        print(f"==== {try_num} HEALTH CHECK FAILED ====\n")
        return health_check_on_launch(serial, test_mode, try_num + 1)

    else:
        return False
