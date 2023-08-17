class InstructionsHandler:
    import time
    import rpi_config
    clock = time.time()
    stages = rpi_config.stages
    stage = stages[0]
    instructions = rpi_config.instructions
    collection = rpi_config.collection
    correction_multipliers = rpi_config.correction_multipliers

    def next_stage(self):
        self.clock = self.clock + self.stage["time"]
        self.stages.pop(0)
        if (len(self.stages) > 0):
            self.stage = self.stages[0]
        else:
            self.stage = False

    def get_correction_degrees(self, current, target):
        plus_c = target - current + 360
        plus = target - current
        minus_c = current - target + 360
        minus = current - target
        if (plus >= 0 and plus <= 180):
            return plus
        if (plus_c >= 0 and plus_c <= 180):
            return plus_c
        if (minus >= 0 and minus <= 180):
            return -minus
        if (minus_c >= 0 and minus_c <= 180):
            return -minus_c
        return 0

    def calculate_instruction_from_correction_degrees(self, correction, sensor):
        if (correction > -5 and correction < 5):
            return 1500
        return self.correction_multipliers[sensor](correction)

    def update_instructions(self, sensors):
        yaw_correction = self.get_correction_degrees(
            current=int(sensors["he"]), target=(self.stage["yaw"]))
        self.instructions["yaw"] = self.calculate_instruction_from_correction_degrees(
            correction=yaw_correction, sensor="yaw")
        self.collection = self.rpi_config.collection
