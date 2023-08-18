test_mode = True

stages = [
    {
        "time": 15,
        # height to add in meters, can be negative.
        # TODO add hg to sensors, add sensor (physical)
        "hg": 0.5
    },
    {
        "time": 15,
        "yw": 0  # yaw in degrees according to abs north, 0 to 360 degrees
    },
    {
        "time": 15,
        "yw": 180
    },
    {
        "time": 15,
        "yw": 90
    },
    {
        "time": 15,
        "yw": 270
    },
    {
        "time": 15,
        "hg": -0.5
    },
]

instructions = {
    "th": 1000,
    "rl": 1500,
    "pt": 1500,
    "yw": 1500,
    "fm": 0
}

instructions_serial_chars = {
    "th": "t",
    "rl": "r",
    "pt": "p",
    "yw": "y",
    "fm": "f"
}

instructions_line = "t1000 r1500 p1500 y1500 f0"

sensor_primitive_values = ["ax", "ay", "az", "mx", "my", "mz"]

correction_multipliers = {
    "yw": lambda degree: 1550 + round(degree / 2) if degree > 0 else 1450 + round(degree / 2)
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

health_check_on_launch = {
    "num_of_tries": 10,
    "num_of_sensor_cycles": 30,
    "sensor_cycle_time_sleep": 0.05,
    "pitch_roll_error_degrees": 3,
    "sensor_error_percents": 0.05
}
