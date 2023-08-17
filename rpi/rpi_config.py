test_mode = True

stages = [
    {
        "time": 15,
        "yaw": 0
    },
    {
        "time": 15,
        "yaw": 180
    },
    {
        "time": 15,
        "yaw": 90
    },
    {
        "time": 15,
        "yaw": 270
    }
]

instructions = {
    "yaw": 0
}

sensor_primitive_values = ["ax", "ay", "az", "mx", "my", "mz"]

correction_multipliers = {
    "yaw": lambda degree: 1550 + round(degree / 2) if degree > 0 else 1450 + round(degree / 2)
}

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
launch_health_checks_num = 3
horizontal_position_error = 3
health = {
    "num_of_tries": 10,
    "num_of_sensor_cycles": 30,
    "sensor_cycle_time_sleep": 0.05,
    "pitch_roll_error_degrees": 3,
    "sensor_error_percents": 0.05
}

collection = {
    "he": [],
    "ax": [],
    "ay": [],
    "az": [],
    "mx": [],
    "my": [],
    "mz": [],
    "pt": [],
    "rl": []
}

health_check_on_launch = {
    "num_of_tries": 10,
    "num_of_sensor_cycles": 30,
    "sensor_cycle_time_sleep": 0.05,
    "pitch_roll_error_degrees": 3,
    "sensor_error_percents": 0.05
}
