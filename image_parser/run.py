from serial import Serial
import time
import pickle
from config import FREQ


class Draw(object):
    def __init__(self, port: Serial):
        self.port = port
        with open("output/steps.pkl", "rb") as f:
            self.steps = pickle.load(f)

    def run(self):
        for item in self.steps:
            left = item[0]
            right = item[1]
            self.port.write(bytes("{:05d}{:05d}".format(left, right), "ascii"))
            print("L - {:05d} R - {:05d}".format(left, right))
            time.sleep(1/FREQ)


if __name__ == "__main__":
    port = Serial(port="COM14", baudrate=115200, timeout=5)
    draw = Draw(port)
    time.sleep(2)
    draw.run()
