import random


def error():
    return random.randint(-5, 5)


def create_serial_object(test_mode):
    if (test_mode):
        class serial:
            he = 220
            ax = 250
            ay = 270
            az = 14000
            mx = -280
            my = 200
            mz = -320

            def readLine(self):
                return f"he{self.he + error()} ax{self.ax + error()} ay{ self.ay + error() } az{self.az +  + error()} mx{self.mx + error()} my{self.my + error()} mz{self.mz + error()}"

            def write(self, line):
                # HARDCODED, FOR TESTS ONLY
                yaw = round((int(line) - 1500) / 20)
                self.he += yaw
                if self.he > 360:
                    self.he = self.he - 360
                if self.he < 0:
                    self.he = self.he + 360
                print(f"Compass degrees: {self.he}")
                print(f"Instructions sent: 'yaw: {line}'")

        print("========== TEST MODE ==========\n")
        return serial()
    else:
        print("========= FLIGHT MODE =========\n")

        import serial
        return serial.Serial(
            port="/dev/ttyAMA0",
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0.1,
        )
