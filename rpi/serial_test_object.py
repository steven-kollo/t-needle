import random


def randint():
    return random.randint(-10, 10)


def create_serial_test_object():
    class serial:
        def readLine(self):
            return f"he{220 + randint()} ax{250 + randint()} ay{ 270 + randint() } az{14000 +  + randint()} mx{-280 + randint()} my{200 + randint()} mz{-320 + randint()}"

        def write(self, line):
            print(f"Instructions sent: '{line}'")

    print("========== TEST MODE ==========\n")
    return serial()
