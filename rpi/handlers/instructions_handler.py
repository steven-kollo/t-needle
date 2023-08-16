class InstructionsHandler:
    import handlers.sensors_handlers as sensors_handlers
    import rpi_config
    instructions = rpi_config.instructions
    collection = rpi_config.collection
    correction_multipliers = rpi_config.correction_multipliers

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

    def update_instructions(self, sensors, stage):
        yaw_correction = self.get_correction_degrees(
            current=int(sensors["he"]), target=(stage["yaw"]))
        self.instructions["yaw"] = self.calculate_instruction_from_correction_degrees(
            correction=yaw_correction, sensor="yaw")
        self.collection = self.rpi_config.collection
