class HealthHandler():
    import rpi_config
    config = rpi_config.health
    launch_health = False
    launch_health_checks_num = rpi_config.launch_health_checks_num
    horizontal_position_error = rpi_config.horizontal_position_error
    history = []
    log = {}
    log_len = 0

    def __init__(self):
        for sensor in self.rpi_config.sensors:
            if sensor in self.rpi_config.sensor_primitive_values:
                self.log[sensor] = []

    def append_sensors_to_health_log(self, sensors):
        self.log_len = self.log_len + 1
        for sensor in self.log:
            self.log[sensor].append(sensors[sensor])

    def get_sensor_mod_vs_peaks_error(self, sensor, mod_num):
        mod = self.log[sensor][mod_num]
        highest_error = self.log[sensor][self.log_len - 1] / mod - 1
        lowest_error = -(self.log[sensor][1] / mod - 1)
        return abs((highest_error + lowest_error) / 2 * 100)

    # def check_launch_position(self):
    #     error = self.horizontal_position_error
    #     pitch_avg = sum(self.log['pt']) / len(self.log['pt'])
    #     roll_avg = sum(self.log['rl']) / len(self.log['rl'])
    #     print(
    #         f"------ Pitch: {round(pitch_avg)} Roll: {round(roll_avg)} ------\n")
    #     if (pitch_avg < error and pitch_avg > -error and roll_avg < error and roll_avg > -error):

    #         print("-------- Pitch Roll OK --------")
    #         print(
    #             f"------ Pitch: {round(pitch_avg)} Roll: {round(roll_avg)} ------\n")
    #         return True
    #     else:
    #         print(
    #             f"------ Pitch: {round(pitch_avg)} Roll: {round(roll_avg)} ------\n")
    #         return False

    def check_health(self):
        avg_error = []
        mod_num = round(self.log_len / 2)
        for sensor in self.log:
            self.log[sensor].sort()
            error = self.get_sensor_mod_vs_peaks_error(
                sensor=sensor, mod_num=mod_num)
            avg_error.append(error)
        avg_error = sum(avg_error)/len(avg_error)
        self.history.append(avg_error)
        print(f"------- Avg error is {round(avg_error)}% -------")
        if self.launch_health == False and len(self.history) >= self.launch_health_checks_num:
            print("\n======= HEALTH CHECK OK =======\n")
            self.launch_health = True

            # print(self.check_launch_position())
            # if self.check_launch_position():
            #     self.launch_health = True
            # else:
            #     print("======== LAUNCH FAILED ========")
            #     self.history = []

    def drop_health_log(self):
        for log in self.log:
            self.log[log] = []
        self.log_len = 0

    def update_health_log(self, sensors):
        if self.log_len < 30:
            self.append_sensors_to_health_log(sensors=sensors)
        else:
            self.check_health()
            self.drop_health_log()
