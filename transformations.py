import math
import numpy as np
import cv2

def calculate_centroid(points):
    area_accumulator = 0
    cx_accumulator = 0
    cy_accumulator = 0

    for i in range(len(points)):
        x0, y0 = points[i]
        x1, y1 = points[(i + 1) % len(points)]  # Ensures the last point connects back to the first

        cross_product = x0 * y1 - x1 * y0
        area_accumulator += cross_product
        cx_accumulator += (x0 + x1) * cross_product
        cy_accumulator += (y0 + y1) * cross_product

    area = 0.5 * area_accumulator
    factor = 1 / (6 * area)

    centroid_x = factor * cx_accumulator
    centroid_y = factor * cy_accumulator

    return centroid_x, centroid_y


def rotate_point(x, y, cx, cy, angle):
    # Translate point to origin
    tempX = x - cx
    tempY = y - cy

    # Rotate point
    rotatedX = tempX * math.cos(angle) - tempY * math.sin(angle)
    rotatedY = tempX * math.sin(angle) + tempY * math.cos(angle)

    # Translate point back
    x = rotatedX + cx
    y = rotatedY + cy
    return x, y

def rotate_shape(points, center, angle, img_width, img_height):
    angle_rad = math.radians(angle)
    rotated_points = [rotate_point(x, y, center[0], center[1], angle_rad) for x, y in points]

    # Check if points are within adjusted image bounds and adjust angle if necessary
    while not all(1 <= pt[0] < img_width - 1 and 1 <= pt[1] < img_height - 1 for pt in rotated_points):
        angle_rad -= math.radians(1)  # Adjust angle by 1 degree
        rotated_points = [rotate_point(x, y, center[0], center[1], angle_rad) for x, y in points]

    return rotated_points, math.degrees(angle_rad)


def shift_shape(points, shift_x, shift_y, img_width, img_height):
    # Calculate the maximum shift allowed to keep all points within bounds with 1-pixel margin
    max_shift_x = min(img_width - 1 - max(x for x, _ in points), max(1 - min(x for x, _ in points), shift_x))
    max_shift_y = min(img_height - 1 - max(y for _, y in points), max(1 - min(y for _, y in points), shift_y))

    # Apply the maximum shift to all points
    shifted_points = [(x + max_shift_x, y + max_shift_y) for x, y in points]

    return shifted_points

import numpy as np

import numpy as np


def resize_shape(points, img_width, img_height, initial_scale_factor, shape_index, rectangle_flag = False):
    if not points:
        return [], 0  # Return empty list and zero scale factor if points are empty

    points_array = np.array(points)
    centroid = np.mean(points_array, axis=0)

    # Using squared distances to avoid expensive sqrt operation
    squared_distances = np.sum((points_array - centroid) ** 2, axis=1)
    max_squared_distance = np.max(squared_distances)

    # Early determination of scale factor
    max_possible_scale_factor = min((img_width - 2) ** 2, (img_height - 2) ** 2) / (2 * max_squared_distance)

    # Adjust scale factor for shape_index 6
    if shape_index == 6:
        max_possible_scale_factor = min(max_possible_scale_factor,
                                        1.5 ** 2)  # Cap the scale factor at 1.5 for shape_index 6
    if shape_index in [0, 3, 5]:
        max_possible_scale_factor = min(max_possible_scale_factor,
                                        2.0 ** 2)  # Cap the scale factor at 1.5 for shape_index 6
    if shape_index == 1:
        max_possible_scale_factor = min(max_possible_scale_factor,
                                        2.2 ** 2)  # Cap the scale factor at 1.5 for shape_index 6
    if initial_scale_factor >= max_possible_scale_factor:
        return points, 1

    scale_factor = min(initial_scale_factor, np.sqrt(max_possible_scale_factor))

    # In-place operations for scaling
    points_array -= centroid
    points_array *= scale_factor
    points_array += centroid

    # In-place clipping
    np.clip(points_array, 1, [img_width - 2, img_height - 2], out=points_array)


    return points_array.tolist(), scale_factor


def apply_motion_blur(image, blur_strength, direction):
    # Creating the motion blur kernel
    if direction.lower() == 'horizontal':
        kernel = np.zeros((blur_strength, blur_strength))
        kernel[int((blur_strength - 1) / 2), :] = np.ones(blur_strength)
    elif direction.lower() == 'vertical':
        kernel = np.zeros((blur_strength, blur_strength))
        kernel[:, int((blur_strength - 1) / 2)] = np.ones(blur_strength)
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'")

    kernel = kernel / blur_strength

    # Apply the motion blur kernel
    blurred_image = cv2.filter2D(image, -1, kernel)

    return blurred_image