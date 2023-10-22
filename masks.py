import numpy as np
import cv2
def mask(color):
    if color == "BLACK":
        return 'bruh'
    elif color == "WHITE":
        return "mbruh"
    elif color == "RED":
        return "mbruh"
    elif color == "ORANGE":
        lowerbound1 = np.array([11, 0, 197])
        upperbound1 = np.array([28, 255, 255])
        return "mbruh"
    elif color == "BROWN":
        lowerbound1 = np.array([0, 0, 102])
        upperbound1 = np.array([11, 255, 255])
        lowerbound2 = np.array([11, 0, 0])
        upperbound2 = np.array([28, 255, 197])
        lowerbound3 = np.array([156, 0, 102])
        upperbound3 = np.array([181, 255, 255])
        mask1 = cv2.inRange(segmented_image, lowerbound1, upperbound1)
        result1 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask1)
        mask2 = cv2.inRange(segmented_image, lowerbound2, upperbound2)
        result2 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask2)
        return "ORANGE"
    elif color == "GREEN":
        return "BROWN"
    elif color == "BLUE":
        return "mbruh"
    elif color == "PURPLE":
        return "mbruh"


