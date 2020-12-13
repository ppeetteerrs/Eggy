import cv2 as cv
import numpy as np
import math


def filterContours(contours: list):
    # Sort contours in descending size
    sorted_contours = sorted(contours, key=lambda x: cv.contourArea(x))

    # Filter out overlapping contours (primitive, use bounding rect)
    filtered_contours = list()
    for contour in sorted_contours:
        if len(filtered_contours) == 0:
            filtered_contours.append(contour)
        else:
            intersected = False
            rect = cv.boundingRect(contour)
            for bigger in filtered_contours:
                bigger_rect = cv.boundingRect(bigger)
                if intersect(rect, bigger_rect):
                    intersected = True
                    break
            if not intersected:
                filtered_contours.append(contour)

    return sorted(filtered_contours, key=lambda x: - cv.boundingRect(x)[0] - cv.boundingRect(x)[1])


def intersect(a, b):
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    w = min(a[0]+a[2], b[0]+b[2]) - x
    h = min(a[1]+a[3], b[1]+b[3]) - y
    return w > 0 and h > 0
