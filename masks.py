import cv2
import numpy as np

def create_masks(image, color, color_data):
    mask = 0
    for color_name, count, percentage, label, hsv in color_data:
        if color_name == color:
            mask += cv2.inRange(image, np.array(hsv), np.array(hsv))
    return mask

def create_masks_test(image, color, color_data, bruh):
    mask = 0
    iterator = 0
    for color_name, count, percentage, label, hsv in color_data:
        if color_name == color and iterator < bruh:
            mask += cv2.inRange(image, np.array(hsv), np.array(hsv))
            iterator += 1
    return mask