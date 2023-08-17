class SensorsHandler:
    import math
    import rpi_config

    def __init__(self):
        self.sensors = self.rpi_config.sensors
        if self.rpi_config.test_mode:
            self.decode_line = self.decode_line_test

    def stringToDictValue(self, sensor):
        self.sensors[sensor[:2]] = int(sensor[2:])

    def calculate_pitch_roll(self):
        math = self.math
        ax = self.sensors["ax"]
        ay = self.sensors["ay"]
        az = self.sensors["az"]
        pitch = -(math.atan2(ax, math.sqrt(ay * ay + az * az))*180.0)/math.pi
        roll = (math.atan2(ay, az)*180.0)/math.pi
        self.sensors["pt"] = pitch
        self.sensors["rl"] = roll

    def decode_line(self, line):
        line.decode("UTF-16", errors='ignore')
        cleaned_bytes = line.replace(b'\r', b'').replace(b'\n', b'')
        return cleaned_bytes.decode()

    def decode_line_test(self, line):
        return line

    def parse_sensors_line(self, line):
        line = self.decode_line(line)
        try:
            for sensor in line.split(" "):
                self.stringToDictValue(sensor)
            self.calculate_pitch_roll()
        except:
            pass
