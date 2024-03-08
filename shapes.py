import cv2
import numpy as np
import math
from PIL import Image, ImageDraw, ImageFont

# Generate shapes
"""
class Shape:
    def __init__(self, img_width, img_height, letter="A"):
"""

def calculate_centroid(points):
    x_coords = [x for x, _ in points]
    y_coords = [y for _, y in points]
    centroid_x = sum(x_coords) / len(points)
    centroid_y = sum(y_coords) / len(points)
    return centroid_x, centroid_y

# Shift points to center
def shift_points_to_center(points, img_width, img_height):
    centered_points = [(x + img_width // 2, y + img_height // 2) for x, y in points]
    return centered_points

def generate_centered_rectangle(width, height, img_width, img_height):
    # Rectangle centered at origin
    half_width, half_height = width / 2, height / 2
    return shift_points_to_center([(-half_width, -half_height), (half_width, -half_height),
            (half_width, half_height), (-half_width, half_height), (-half_width, -half_height)], img_width, img_height)


def generate_centered_cross(vertical_length, horizontal_length, thickness, img_width, img_height):
    v_half = vertical_length / 2
    h_half = horizontal_length / 2
    t_half = thickness / 2

    # Points are ordered to draw the cross without intersecting lines
    points = [
        (-h_half, -t_half), (-t_half, -t_half), # Start of horizontal left to vertical top
        (-t_half, -v_half), (t_half, -v_half),  # Vertical top to bottom
        (t_half, -t_half), (h_half, -t_half),   # Vertical bottom to horizontal right
        (h_half, t_half), (t_half, t_half),     # Horizontal right to vertical bottom
        (t_half, v_half), (-t_half, v_half),    # Vertical bottom to top
        (-t_half, t_half), (-h_half, t_half),   # Vertical top to horizontal left
        (-h_half, -t_half)  # Close the horizontal left
    ]

    return shift_points_to_center(points, img_width, img_height)


def generate_centered_star(outer_radius, inner_radius, num_points, img_width, img_height):
    points = []
    offset_angle = -math.pi / 2  # Adjust the starting angle to point upwards
    for i in range(num_points):
        # Outer point (tip of the star)
        angle = offset_angle + 2 * math.pi * i / num_points
        x = outer_radius * math.cos(angle)
        y = outer_radius * math.sin(angle)
        points.append((x, y))

        # Inner point
        inner_angle = angle + math.pi / num_points
        x_inner = inner_radius * math.cos(inner_angle)
        y_inner = inner_radius * math.sin(inner_angle)
        points.append((x_inner, y_inner))

    points.append(points[0])

    return shift_points_to_center(points, img_width, img_height)



def generate_centered_circle(radius, num_points, img_width, img_height):
    points = [(radius * math.cos(2 * math.pi / num_points * i),
      radius * math.sin(2 * math.pi / num_points * i)) for i in range(num_points)]
    points.append(points[0])
    return shift_points_to_center(points , img_width, img_height)

def generate_centered_semi_circle(radius, num_points, img_width, img_height):
    points = []
    for i in range(num_points + 1):  # Include the last point
        angle = math.pi * (i / num_points)  # Angle from 0 to π radians
        x = radius * math.cos(angle)
        y = -radius * math.sin(angle) + radius / 2  # Shift upwards by radius / 2
        points.append((x, y))
    points.append(points[0])
    return shift_points_to_center(points, img_width, img_height)

def generate_centered_pentagon(radius, img_width, img_height):
    points = []
    offset_angle = -math.pi / 2  # Start from the top
    for i in range(5):
        angle = offset_angle + 2 * math.pi * i / 5  # Adjust angle for top alignment
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        points.append((x, y))
    points.append(points[0])
    return shift_points_to_center(points, img_width, img_height)



def generate_centered_quarter_circle(radius, num_points, img_width, img_height):
    points = []
    for i in range(num_points + 1):
        angle = math.pi / 2 * i / num_points  # Angle from 0 to π/2 radians
        x = radius * math.cos(angle)
        y = -radius * math.sin(angle)
        points.append((x - radius / 2, y + radius / 2))  # Shift to make geometric center at origin
    points.append((-radius / 2, radius / 2))  # Include the last point
    points.append(points[0])
    return shift_points_to_center(points, img_width, img_height)



def generate_centered_triangle(side_length, img_width, img_height):
    height = side_length * (math.sqrt(3) / 2)
    points = [(-side_length / 2, height / 3), (0, -2 * height / 3), (side_length / 2, height / 3)]
    points.append(points[0])
    return shift_points_to_center(points, img_width, img_height)


# Draw shape
def draw_shape(img, points, color=(255, 0, 0), thickness=2):
    num_points = len(points)
    for i in range(num_points):
        start_point = tuple(map(int, points[i]))
        end_point = tuple(map(int, points[(i + 1) % num_points]))
        cv2.line(img, start_point, end_point, color, thickness)

def fill_shape(img, points, color=(255, 0, 0)):
    # Ensure points are in the correct format for fillPoly
    pts = np.array([points], dtype=np.int32)
    cv2.fillPoly(img, pts, color)




def addTextWithPillow(main_cv2_img, text, font_path, centroid, font_size, angle, scale_factor=1.0, alphanum_color=(255, 255, 255)):
    # Convert the cv2 image to a PIL image
    main_img = Image.fromarray(cv2.cvtColor(main_cv2_img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(main_img)
    font = ImageFont.truetype(font_path, int(font_size * scale_factor))

    # Get text width and height
    text_width = int(draw.textlength(text, font=font))
    text_height = int(font.getmask(text).getbbox()[3])

    # Increase the canvas size slightly to account for rotation
    canvas_width = text_width + 20
    canvas_height = text_height + 20

    # Create an image for the text with slightly extra space
    text_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    # Draw text in the center of the new canvas
    text_draw.text(((canvas_width - text_width) // 2, (canvas_height - text_height) // 2), text, font=font, fill=alphanum_color)

    # Rotate the text image
    rotated_text_img = text_img.rotate(-angle, expand=1)
    rotated_width, rotated_height = rotated_text_img.size

    # Adjust position for rotation
    dx = (rotated_width - canvas_width) / 2
    dy = (rotated_height - canvas_height) / 2
    adjusted_x = centroid[0] - rotated_width // 2
    adjusted_y = centroid[1] - rotated_height // 2

    # Apply specific offsets based on angle
    if 0 < angle < 90:
        adjusted_x += 10
        adjusted_y -= 15
    elif angle == 90:
        adjusted_x += 10
    elif 90 < angle < 180:
        adjusted_x += 10
        adjusted_y += 15
    elif angle == 180:
        adjusted_y += 15
    elif 180 < angle < 270:
        adjusted_x -= 10
        adjusted_y += 15
    elif angle == 270:
        adjusted_x -= 10
    elif 270 < angle < 360:
        adjusted_x -= 10
        adjusted_y -= 15
    elif angle == 360 or angle == 0:
        adjusted_y -= 15

    # Paste the rotated text image onto the main image
    main_img.paste(rotated_text_img, (int(adjusted_x), int(adjusted_y)), rotated_text_img.split()[3])

    # Convert the PIL image back to a cv2 image
    cv2_image = np.array(main_img)
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)

    return cv2_image

def specialAddText(main_cv2_img, text, font_path, centroid, font_size, angle, scale_factor=1.0, alphanum_color=(255, 255, 255)):
    # Convert the cv2 image to a PIL image
    main_img = Image.fromarray(cv2.cvtColor(main_cv2_img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(main_img)
    font = ImageFont.truetype(font_path, int(font_size * scale_factor))

    # Get text width and height
    text_width = int(draw.textlength(text, font=font))
    text_height = int(font.getmask(text).getbbox()[3])

    # Increase the canvas size slightly to account for rotation
    canvas_width = text_width + 30
    canvas_height = text_height + 30

    # Create an image for the text with slightly extra space
    text_img = Image.new('RGBA', (canvas_width, canvas_height), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    # Draw text in the center of the new canvas
    text_draw.text(((canvas_width - text_width) // 2, (canvas_height - text_height) // 2), text, font=font, fill=alphanum_color)

    # Rotate the text image
    rotated_text_img = text_img.rotate(-angle, expand=1)
    rotated_width, rotated_height = rotated_text_img.size

    # Adjust position for rotation
    dx = (rotated_width - canvas_width) / 2
    dy = (rotated_height - canvas_height) / 2
    adjusted_x = centroid[0] - rotated_width // 2
    adjusted_y = centroid[1] - rotated_height // 2


    # Paste the rotated text image onto the main image
    main_img.paste(rotated_text_img, (int(adjusted_x -10), int(adjusted_y - 10)), rotated_text_img.split()[3])

    # Convert the PIL image back to a cv2 image
    cv2_image = np.array(main_img)
    cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)

    return cv2_image

