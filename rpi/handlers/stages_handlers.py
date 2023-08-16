def next_stage(stages, stage, clock):
    clock = clock + stage["time"]
    stages.pop(0)
    if (len(stages) > 0):
        stage = push_stage(stages)
    else:
        stage = False

    return {
        "stages": stages,
        "stage": stage,
        "clock": clock
    }


def push_stage(stages):
    return {
        "time": stages[0]["time"],
        "yaw": stages[0]["yaw"]
    }
