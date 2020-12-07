import cv2 as cv
import numpy as np
import math
import pickle
import random

# --------------------------------- Settings --------------------------------- #
IMAGE_DIM = 1000  # M,N
BUFFER_DIAG = 120
DRAW_DIAG = 70
TOTAL_DIAG = 200
assert BUFFER_DIAG + DRAW_DIAG < TOTAL_DIAG, "Diagonals Contraints Violated"

INIT_OCR_VAL = 1400
OCR_STEP_SIZE = 10

buffer_side = BUFFER_DIAG / math.sqrt(2)
draw_side = DRAW_DIAG / math.sqrt(2)
print("Buffer Side Length: {:.2f}, Draw Side Length: {:.2f}".format(buffer_side, draw_side))

# -------------------------------- Read Image -------------------------------- #
srcImg = cv.imread("input/people.jpg")

# ------------------- Resize Image and Turn Black and White ------------------ #
w, h, _ = srcImg.shape
crop_length = h if w > h else w
srcImg = srcImg[:crop_length, :crop_length, :]
bwImg = cv.cvtColor(srcImg, cv.COLOR_BGR2GRAY)
blurred = cv.GaussianBlur(bwImg, (3, 3), 0)
blurred = cv.resize(blurred, (IMAGE_DIM, IMAGE_DIM))
cv.imwrite("output/resized.png", blurred)

# ---------------------------- Extract Image Edges --------------------------- #
median = np.median(blurred)
lower = int(max(0, (1.0 - 0.33) * median))
upper = int(min(255, (1.0 + 0.33) * median))
edgeImg = cv.Canny(blurred, lower, upper)
blank2 = np.zeros((edgeImg.shape[0], edgeImg.shape[1], 1), np.uint8)
cv.circle(blank2, (500, 500), 300, 255, 1)

# -------------------------- Extrace Image Contours -------------------------- #
contours, hierarchy = cv.findContours(blank2, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
blank = np.zeros((edgeImg.shape[0], edgeImg.shape[1], 3), np.uint8)
contourImg = cv.drawContours(blank, contours, -1, (0, 255, 0), 1)
cv.imwrite("output/contours.png", blank2)
print("{} Contours Found".format(len(contours)))

# -------------------- Convert Coordinates to Joint Angles ------------------- #
joint_steps = list()
for contour in contours:
    contour = contour.tolist()
    contour.append(contour[len(contour) - 1])
    for coord in contour:
        # (m,n) --> (x,y)
        m, n = coord[0]
        x = m / IMAGE_DIM * draw_side + buffer_side
        y = n / IMAGE_DIM * draw_side + buffer_side
        # (x,y) --> (theta, alpha)
        theta = np.arctan2(y, x)
        r = math.sqrt(x ** 2 + y ** 2)
        alpha = np.arccos(r / 200)
        # (theta, alpha) --> (theta1, theta2)
        theta1 = math.pi / 4 + alpha - theta
        theta2 = alpha + theta - math.pi / 4
        # (theta1, theta2) --> (ocr1a, ocr1b)
        ocr1a = theta2 / math.pi * 4000 + 1000
        ocr1b = theta1 / math.pi * 4000 + 1000
        assert ocr1a <= 4000 and ocr1b <= 4000, "Joint Constraint Vioalted"
        joint_steps.append((ocr1a, ocr1b))

# ----------------------------- Calculate Deltas ----------------------------- #
joint_deltas = list()
last_ocr1a = INIT_OCR_VAL
last_ocr1b = INIT_OCR_VAL
for step in joint_steps:
    last_index = len(joint_deltas) - 1
    ocr1a_steps = int(round((step[0] - last_ocr1a) / OCR_STEP_SIZE, 0))
    ocr1b_steps = int(round((step[1] - last_ocr1b) / OCR_STEP_SIZE, 0))
    ocr1a_step_cnt = abs(ocr1a_steps)
    ocr1b_step_cnt = abs(ocr1b_steps)
    max_step = list(range(max([ocr1a_step_cnt, ocr1b_step_cnt])))
    print(max_step)
    ocr1a_can_step = random.choices(max_step, k=ocr1a_step_cnt)
    ocr1b_can_step = random.choices(max_step, k=ocr1b_step_cnt)
    for i in max_step:
        ocr1a_val = 1
        if i in ocr1a_can_step:
            ocr1a_val = 2 if ocr1a_steps > 0 else 0
        ocr1b_val = 1
        if i in ocr1b_can_step:
            ocr1b_val = 2 if ocr1b_steps > 0 else 0
        joint_deltas.append([ocr1a_val, ocr1b_val])
    last_ocr1a += ocr1a_steps * OCR_STEP_SIZE
    last_ocr1b += ocr1b_steps * OCR_STEP_SIZE
print(joint_deltas[:100])
print("{} Steps Found".format(len(joint_deltas)))
with open("output/steps.pkl", "wb") as f:
    pickle.dump(joint_deltas, f)
