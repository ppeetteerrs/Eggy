import cv2 as cv
import numpy as np
import math
import pickle
import random
import matplotlib.pyplot as plt
from transform import ServoCtrl
from config import IMAGE_DIM, DRAW_DIM, BUFFER_DIM, DIST_THRES, AREA_THRES
# Crop Image to Square
srcImg = np.zeros((IMAGE_DIM, IMAGE_DIM, 3), np.uint8)
cv.putText(srcImg, "hi", (50, 850), cv.FONT_HERSHEY_SIMPLEX, 30, (255, 255, 255), 90, cv.LINE_AA)
srcImg = cv.flip(srcImg, 0)

# Blur, Convert to Grayscale and Threshold
bwImg = cv.cvtColor(srcImg, cv.COLOR_BGR2GRAY)
cv.imwrite("output/src.png", bwImg)

# Find Connected Components
contours, _ = cv.findContours(bwImg, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

# Draw Contours
blank = np.zeros((bwImg.shape[0], bwImg.shape[1], 3), np.uint8)
cv.drawContours(blank, contours, -1, (0, 255, 0), 1)
print("{} Contours Found".format(len(contours)))
cv.imwrite("output/contours.png", blank)

# -------------------- Convert Coordinates to Joint Angles ------------------- #
servoCtrl = ServoCtrl(contours)
servoCtrl.spit()
# servoCtrl.plotPolar()
