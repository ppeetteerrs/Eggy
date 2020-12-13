import cv2 as cv
import numpy as np
import math
import pickle
import random
from config import IMAGE_DIM, DRAW_DIM, BUFFER_DIM, DIST_THRES, STEP_DIST, TOTAL_DIM
import matplotlib.pyplot as plt


class ServoCtrl(object):
    def __init__(self, contours):
        super().__init__()
        # Polar Plot Data
        self.plotData = {
            "r": list(),
            "t": list(),
            "i": list()
        }

        # Transformations
        self.pointsMN = self.genPoints(contours)  # (m, n, i) - (pixel row, pixel col, column index)
        self.pointsXY = self.genXY(self.pointsMN)  # (x, y, i) in Cartesian coordinates
        self.pointsPolar = self.genPolar(self.pointsXY)  # (r, theta, alpha, i) in Polar coordinates (alpha is angle between two arms / 2)
        self.pointsAngle = self.genAngle(self.pointsPolar)  # (theta_l, theta_r, i) in Servo angles (from line y=x)
        self.pointsCnt = self.genCnt(self.pointsAngle)  # (cnt_l, cnt_r, i) in Servo timer count

    def genPoints(self, contours):
        points = list()
        for i, contour in enumerate(contours):
            contour_list = contour.tolist()
            # Append starting point to end of each contour
            contour_list.append(contour_list[0])
            # Copy over points with contour info
            points.extend([(coord[0][0], coord[0][1], i+1) for coord in contour])
        return points

    def genXY(self, points):
        # Filter out points with distance < DIST_THRES from previous point
        last = None  # Add initial position
        xy_filtered = list()
        for m, n, i in points:
            x = m / IMAGE_DIM * DRAW_DIM + BUFFER_DIM
            y = n / IMAGE_DIM * DRAW_DIM + BUFFER_DIM
            # Distance from last point
            if last:
                distance = math.sqrt((x - last[0]) ** 2 + (y - last[1]) ** 2)
                if distance > DIST_THRES:
                    last = (x, y, i)
                    xy_filtered.append(last)
            else:
                # First point in the list
                last = (x, y, i)
                xy_filtered.append(last)
        # Add interpolated steps
        last = (TOTAL_DIM, TOTAL_DIM, 0)
        xy = [last]
        for x, y, i in xy_filtered:
            # Distance from last point
            change_x = x - last[0]
            change_y = y - last[1]
            distance = math.sqrt(change_x ** 2 + change_y ** 2)
            interpolate_steps = math.ceil(distance / STEP_DIST)
            assert interpolate_steps > 0, "Something Weird"
            dx = change_x / interpolate_steps
            dy = change_y / interpolate_steps
            for t in range(1, interpolate_steps):
                inter_x = last[0] + dx * t
                inter_y = last[1] + dy * t
                xy.append((inter_x, inter_y, i))
            last = (x, y, i)
            xy.append((x, y, i))
        return xy

    def genPolar(self, points):
        polar = list()
        for x, y, i in points:
            r = math.sqrt(x ** 2 + y ** 2)
            assert r < 200, "A bit too far man"
            t = np.arctan2(y, x)
            a = np.arccos(r / 200)
            polar.append((r, t, a, i))
            self.plotData["r"].append(r)
            self.plotData["t"].append(t)
            self.plotData["i"].append(i)
        return polar

    def genAngle(self, points):
        return [(a + t - math.pi / 4, 2 * a, i) for _, t, a, i in points]

    def genCnt(self, points):
        cnt = list()
        for tl, tr, i in points:
            cntl = int(round(tl/math.pi * 2000 + 500, 0))
            cntr = int(round((tr - tl)/math.pi * 2000 + 500, 0))
            cntl = max(500, min(cntl, 1400))
            cntr = max(500, min(cntr, 1400))
            cnt.append((cntl, cntr, i))
        return cnt

    def plotPolar(self):
        ax = plt.subplot(111, projection='polar')
        ax.scatter(self.plotData["t"], self.plotData["r"], c=self.plotData["i"], s=1, cmap="hsv", alpha=0.3)
        ax.grid(True)
        ax.set_thetamin(0)
        ax.set_thetamax(90)
        ax.set_title("Polar Plot", va='bottom')
        plt.show()

    def spit(self):
        print("{} Steps Found".format(len(self.pointsCnt)))
        print(self.pointsCnt[:20])
        with open("output/steps.pkl", "wb") as f:
            pickle.dump(self.pointsCnt, f)
