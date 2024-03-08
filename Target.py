import cv2
import math
import random
import numpy as np
from shapes import generate_centered_rectangle, generate_centered_cross, generate_centered_star, generate_centered_circle, generate_centered_quarter_circle, generate_centered_semi_circle, generate_centered_triangle, generate_centered_pentagon, draw_shape, fill_shape, addTextWithPillow, specialAddText
from transformations import rotate_shape, shift_shape, resize_shape, apply_motion_blur, calculate_centroid
from utils import createLabel, normalize_coordinates, plot_contour, mapShapesToNumber

def pick_random_color():
    White = (255, 255, 255)
    Black = (0, 0, 0)
    Red = (255, 0, 0)
    Blue = (0, 0, 255)
    Green = (0, 255, 0)
    Purple = (128, 0, 128)
    Brown = (150, 75, 0)
    Orange = (255, 165, 0)
    colors = [White, Black, Red, Blue, Green, Purple, Brown, Orange]
    color = colors[random.randint(0, 7)]
    return color

def pick_random_alphanum():
    letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q",
               "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    return letters[random.randint(0, 35)]
def create_target_image(shape_index, bg_img):
    bg_img_copy = np.copy(bg_img)
    bg_img_height, bg_img_width, channels = bg_img_copy.shape
    global_rotation_angle = random.randint(0, 360)
    global_scale_factor = random.uniform(1,2.8)
    shift_x = random.choice([-1,1]) * random.randint(0, int(bg_img_width/3/(2*global_scale_factor)))
    print("Shift in X Direction:", shift_x)
    shift_y = random.choice([-1, 1]) * random.randint(0, int(bg_img_height / 3 / (2 * global_scale_factor)))

    print("Shift in Y Direction:", shift_y)
    alphanum_color = tuple(reversed(pick_random_color()))
    shape_color = tuple(reversed(pick_random_color()))
    alphanum = pick_random_alphanum()
    while alphanum_color == shape_color:
        alphanum_color = tuple(reversed(pick_random_color()))
        shape_color = tuple(reversed(pick_random_color()))
    print(shape_color)
    print(alphanum_color)
    if shape_index == 0:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_circle(50, 100, bg_img_width, bg_img_height)
    elif shape_index == 1:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_cross(120, 120, 40, bg_img_width, bg_img_height)
    elif shape_index == 2:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_pentagon(55,bg_img_width, bg_img_height)
    elif shape_index == 3:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_quarter_circle(75, 100, bg_img_width, bg_img_height)
    elif shape_index == 4:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_rectangle(80, 110, bg_img_width, bg_img_height)
    elif shape_index == 5:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_semi_circle(80, 100, bg_img_width, bg_img_height)
    elif shape_index == 6:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_star(100, 50, 5, bg_img_width, bg_img_height)
    else:
        print(mapShapesToNumber(shape_index))
        shape = generate_centered_triangle(80, bg_img_width, bg_img_height)
    shape = shift_shape(shape, shift_x, shift_y, bg_img_width, bg_img_height)
    shape, scale_factor = resize_shape(shape, bg_img_width, bg_img_height, global_scale_factor, shape_index)
    shape, angle = rotate_shape(shape, (bg_img_width / 2, bg_img_height / 2), global_rotation_angle, bg_img_width, bg_img_height)
    print("Global Rotation Angle 1:", global_rotation_angle)
    print("Global Scale Factor:", global_scale_factor)
    fill_shape(bg_img_copy, shape, shape_color)
    rotated_centroid = calculate_centroid(shape)
    bg_img_copy = addTextWithPillow(bg_img_copy, alphanum, 'calibrib.ttf', rotated_centroid, 45, angle, scale_factor, alphanum_color)
    print("Global Rotation Angle 2:", global_rotation_angle)
    print("Global Scale Factor:", global_scale_factor)
    return bg_img_copy, shape

def create_target_rectangle(shape_index, bg_img):
    alphanum_color = tuple(reversed(pick_random_color()))
    shape_color = tuple(reversed(pick_random_color()))
    alphanum = pick_random_alphanum()
    while alphanum_color == shape_color:
        alphanum_color = tuple(reversed(pick_random_color()))
        shape_color = tuple(reversed(pick_random_color()))
    print(shape_color)
    print(alphanum_color)
    bg_img_copy = np.zeros((320, 320, 3), np.uint8)
    bg_img_copy[:] = shape_color
    bg_img_height, bg_img_width, channels = bg_img_copy.shape
    global_rotation_angle = random.randint(0, 360)
    print(mapShapesToNumber(shape_index))
    shape = generate_centered_rectangle(80, 110, bg_img_width, bg_img_height)
    print(shape)
    bg_img_copy = specialAddText(bg_img_copy, alphanum, 'calibrib.ttf', (bg_img_width/2, bg_img_height/2), 45, global_rotation_angle, 3, alphanum_color)
    return bg_img_copy, shape

