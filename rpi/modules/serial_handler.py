class SerialHandler():
    def __init__(self):
        import rpi_config

        if (rpi_config.test_mode):
            print("\n========== TEST MODE ==========\n")

            # HARDCODED, FOR TESTS ONLY
            class Serial:
                import random
                he = 220
                ax = 250
                ay = 270
                az = 14000
                mx = -280
                my = 200
                mz = -320

                def error(self):
                    return self.random.randint(-5, 5)

                def readLine(self):
                    return f"he{self.he + self.error()} ax{self.ax + self.error()} ay{ self.ay + self.error() } az{self.az +  + self.error()} mx{self.mx + self.error()} my{self.my + self.error()} mz{self.mz + self.error()}"

                # WARNING! BRUTAL HARDCODE, FOR TESTS ONLY
                def write(self, line):
                    yaw = round((int(line) - 1500) / 20)
                    self.he += yaw
                    if self.he > 360:
                        self.he = self.he - 360
                    if self.he < 0:
                        self.he = self.he + 360
                    print(f"Compass degrees: {self.he}")
                    print(f"Instructions sent: 'yaw: {line}'")

            self.Serial = Serial()

        else:
            print("\n========= FLIGHT MODE =========\n")
            import serial
            self.Serial = serial.Serial(
                port="/dev/ttyAMA0",
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0.1,
            )
