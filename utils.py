import cv2
import matplotlib.pyplot as plt
import random
import string
import glob
from roboflow import Roboflow

def generate_random_string(length):
    # Define the characters that can be used in the string
    characters = string.ascii_letters + string.digits  # Includes uppercase, lowercase, and digits
    # Alternatively, you can add string.punctuation for symbols

    # Generate a random string of the specified length
    random_string = ''.join(random.choice(characters) for _ in range(length))

    return random_string
def mapShapesToNumber(shape):
    shapes = {
        0: 'circle',
        1: 'cross',
        2: 'pentagon',
        3: 'quartercircle',
        4: 'rectangle',
        5: 'semicircle',
        6: 'star',
        7: 'triangle'
    }

    return shapes[shape]
def createLabel(shape_index, points, name):
    with open(f'{name}', 'w') as file:
        file.write(f"{shape_index} ")
        # Iterate through each tuple in the list
        for i in range(len(points)):
            # Write the coordinates to the file without parentheses or commas
            if (i != len(points) - 1):
                file.write(f"{points[i][0]} {points[i][1]} ")
            else:
                file.write(f"{points[i][0]} {points[i][1]}")

def normalize_coordinates(coordinates, image_width, image_height):
    normalized_coords = []
    for coord in coordinates:
        normalized_x = round(coord[0] / image_width, 5)
        normalized_y = round(coord[1] / image_height, 5)
        normalized_coords.append((normalized_x, normalized_y))
    return normalized_coords



def plot_contour(contours):
    """
    Plots the points of given CV2 contours and connects them.

    :param contours: A list of contours, where each contour is an array of points.
    """
    for contour in contours:
        # Reshape the contour to remove the extra dimension
        points = contour.reshape(-1, 2)

        # Splitting points into x and y coordinates
        x = points[:, 0]
        y = points[:, 1]

        # Plotting the points
        plt.plot(x, y, marker='o') # 'o' is for circular markers

        # Connecting the points
        plt.plot(x, y)

    # Configure the axes
    plt.gca().invert_yaxis()  # Invert y-axis to match image coordinate system
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('Contour Points')

    # Display the plot
    plt.show()

def upload_to_roboflow(API_KEY, project_id, img_name, label_name, shape_index):
    # Initialize Roboflow client
    rf = Roboflow(api_key=API_KEY)
    print(img_name, label_name)
    # Get the upload project from Roboflow workspace
    project = rf.workspace().project(project_id)
    #with open('label_map.txt', 'w') as file:
    #    file.write(f"{mapShapesToNumber(shape_index)}")
    print(project.single_upload(
        image_path=img_name,
        annotation_path=label_name,
        annotation_labelmap='label_map.txt',
        # split='test',
        # optional parameters:
        # num_retry_uploads=0,
        # batch_name='batch_name',
        # tag_names=['tag1', 'tag2'],
        # is_prediction=False,
    ))

