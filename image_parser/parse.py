import cv2 as cv
import numpy as np
import math
import pickle
import random
import matplotlib.pyplot as plt
from transform import ServoCtrl
from config import IMAGE_DIM, DRAW_DIM, BUFFER_DIM, DIST_THRES, AREA_THRES
from utils import filterContours
# -------------------------------- Read Image -------------------------------- #
srcImg = cv.imread("input/circle.jpg")

# Crop Image to Square
w, h, _ = srcImg.shape
crop_length = h if w > h else w
srcImg = srcImg[:crop_length, :crop_length, :]
srcImg = cv.flip(srcImg, 0)
srcImg = cv.resize(srcImg, (IMAGE_DIM, IMAGE_DIM))
cv.imwrite("output/src.png", srcImg)

# Blur, Convert to Grayscale and Threshold
blurred = cv.GaussianBlur(srcImg, (3, 3), 0)
gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
bwImg = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1]
cv.imwrite("output/bw.png", bwImg)

# Find Connected Components
n_connected, labels = cv.connectedComponents(bwImg, connectivity=8)
contours, _ = cv.findContours(labels, cv.RETR_FLOODFILL, cv.CHAIN_APPROX_SIMPLE)

filtered_contours = filterContours(contours)
# Draw Contours
blank = np.zeros((bwImg.shape[0], bwImg.shape[1], 3), np.uint8)
cv.drawContours(blank, filtered_contours, -1, (0, 255, 0), 1)
print("{} Contours Found".format(len(filtered_contours)))
cv.imwrite("output/contours.png", blank)

# -------------------- Convert Coordinates to Joint Angles ------------------- #
servoCtrl = ServoCtrl(filtered_contours)
servoCtrl.spit()
# servoCtrl.plotPolar()
