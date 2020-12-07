from serial import Serial
import time
import pickle


class Draw(object):
    def __init__(self, port: Serial):
        self.port = port
        with open("output/steps.pkl", "rb") as f:
            self.steps = pickle.load(f)

    def run(self):
        for item in self.steps:
            leftus = item[0]
            rightus = item[1]

            self.port.write(bytes("{}{}".format(leftus, rightus), "ascii"))
            time.sleep(20/1000)


# time.sleep(1)
# for delta in deltas:
#     time.sleep(0.010)
#     ser.write(bytes("l{}\r".format(delta[0]), "ascii"))
#     ser.write(bytes("r{}\r".format(delta[1]), "ascii"))

if __name__ == "__main__":
    port = Serial(port="COM14", baudrate=115200, timeout=5)
    draw = Draw(port)
    time.sleep(2)
    draw.run()
