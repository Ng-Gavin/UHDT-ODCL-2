import math

import cv2
import numpy as np
from Target import create_target_image, create_target_rectangle
from utils import normalize_coordinates, createLabel, generate_random_string, upload_to_roboflow
from transformations import apply_motion_blur, rotate_shape, resize_shape, shift_shape
import random
import os, shutil, time
from shapes import generate_centered_rectangle, generate_centered_cross, generate_centered_star, generate_centered_circle, generate_centered_quarter_circle, generate_centered_semi_circle, generate_centered_triangle, generate_centered_pentagon, draw_shape, fill_shape, addTextWithPillow

def delete_files_in_directory(folder):
   for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

backgrounds = []
num_images = 50
for Bfiles in os.listdir('backgrounds'):
    if Bfiles.endswith('.png'):
        backgrounds.append(Bfiles)


def generate_images_and_labels(num_images):
    base_path = "/Volumes/Ventoy/shape-classification"
    #base_path = "test_dir"
    for i in range(num_images):
        set_number = i // 100
        images_dir = os.path.join(base_path, f'set_{set_number}', 'images')
        labels_dir = os.path.join(base_path, f'set_{set_number}', 'labels')

        # Create directories if they don't exist
        os.makedirs(images_dir, exist_ok=True)
        os.makedirs(labels_dir, exist_ok=True)

        background_index = random.randint(0, len(backgrounds) - 1)
        try:
            img = cv2.imread(os.path.join('backgrounds', backgrounds[background_index]))
            name = generate_random_string(10)
            label_name = os.path.join(labels_dir, f'{name}.txt')
            img_name = os.path.join(images_dir, f'{name}.jpg')
            print(img_name, label_name)
            bg_img_height, bg_img_width, channels = img.shape
            #shape_index = random.randint(0,7)
            shape_index =4
            if shape_index == 4:
                full_size = random.choice([False, False])
                if (full_size == True):
                    target_image, points = create_target_rectangle(4, img)
                    apply_blur = random.choice([False, True])
                    if apply_blur == True:
                        blur_strength = random.randint(0, 85)
                        blur_direction = random.choice(['horizontal', 'vertical'])
                        target_image = apply_motion_blur(target_image, blur_strength, blur_direction)
                    normalized_coords = normalize_coordinates([(0, 0), (320, 0), (320, 320), (0, 320), (0, 0)], bg_img_width, bg_img_height)
                    createLabel(shape_index, normalized_coords, label_name)
                    cv2.imwrite(img_name, target_image)
                else:
                    target_image, points = create_target_image(shape_index, img)
                    apply_blur = random.choice([False, True])
                    if apply_blur == True:
                        blur_strength = random.randint(0, 85)
                        blur_direction = random.choice(['horizontal', 'vertical'])
                        target_image = apply_motion_blur(target_image, blur_strength, blur_direction)
                    normalized_coords = normalize_coordinates([(0, 0), (320, 0), (320, 320), (0, 320), (0, 0)], bg_img_width, bg_img_height)
                    createLabel(shape_index, normalized_coords, label_name)
                    cv2.imwrite(img_name, target_image)
            else:
                target_image, points = create_target_image(shape_index, img)
                apply_blur = random.choice([False, True])
                if apply_blur == True:
                    blur_strength = random.randint(0,90)
                    blur_direction = random.choice(['horizontal', 'vertical'])
                    target_image = apply_motion_blur(target_image, blur_strength, blur_direction)
                normalized_coords = normalize_coordinates(points, bg_img_width, bg_img_height)
                createLabel(shape_index, normalized_coords, label_name)
                cv2.imwrite(img_name, target_image)
            upload_to_roboflow('SVfKNom2r0ObeMMEf6Cq', 'max_set', img_name, label_name, shape_index)
        except:
            print(backgrounds[background_index])

# Call the function with the desired number of images
generate_images_and_labels(1236-637)  # Replace 1000 with your desired number of images

"""
 #Rectanglex
img = np.full((320, 320, 3), (0, 255, 255), np.uint8)
img_height, img_width, channels = img.shape
rectangle_points = generate_centered_rectangle(200, 100, img_width, img_height)
centered_rectangle = rectangle_points
shape, angle = rotate_shape(centered_rectangle, (img_width / 2, img_height / 2), 45, img_width, img_height)
draw_shape(img, shape, (0, 255, 0))
img = apply_motion_blur(img, 20, 'horizontal')
print(shape)
normalized_coords = normalize_coordinates(shape, img_width, img_height)
createLabel(4, normalized_coords, 'labels/test1')
cv2.imwrite('images/test1.jpg', img)
cv2.imshow("Centered Rectangle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""
"""
# Cross
img_width, img_height = 800, 600
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

cross_points = generate_centered_cross(200, 200, 50, img_width, img_height)
centered_cross = cross_points
rotated_cross = rotate_shape(centered_cross, (img_width/2,img_height/2), 30)
scaled_cross = resize_shape(rotated_cross, img_width, img_height, 50)
draw_shape(img, scaled_cross, (0, 0, 255))
#gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Apply thresholding
#_, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

# Find contours
#contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#print(contours)
#contour_points = []
#if contours:
#    first_contour = contours[0]
    # Convert each point in the contour to a tuple and add to a list
#    contour_points = [(int(x), int(y)) for [x, y] in first_contour.squeeze()]
normalized_coords = normalize_coordinates(scaled_cross, img_width, img_height)
createLabel('cross', normalized_coords, 'labels/test2')
#plot_contour(contours)
# Draw contours on the original image
#cv2.drawContours(img, contours, -1, (0, 255, 0), 3)



cv2.imwrite('images/test2.jpg', img)
cv2.imshow("Centered Cross", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Star
img_width, img_height = 800, 600
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

star_outer_radius = min(img_width, img_height) // 4
star_inner_radius = star_outer_radius / 2.5  # Adjust this factor as needed
star_points = generate_centered_star(star_outer_radius, star_inner_radius, 5, img_width, img_height)  # 5-point star
centered_star = star_points
rotated_cross = rotate_shape(centered_star, (img_width/2,img_height/2), 25)
rotated_cross = shift_shape(rotated_cross, 200, 300, img_width, img_height)
draw_shape(img, rotated_cross, (0, 0, 255))
normalized_coords = normalize_coordinates(rotated_cross, img_width, img_height)
createLabel('star', normalized_coords, 'labels/test3')
cv2.imwrite('images/test3.jpg', img)
cv2.imshow("Centered Cross", img)
cv2.waitKey(0)
cv2.destroyAllWindows()




# Circle
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
circle_points = generate_centered_circle(100, 360, img_width, img_height)
centered_circle = circle_points
shift_shape(centered_circle, -100, 400, img_width, img_height)
draw_shape(img, centered_circle, (0, 0, 255))
normalized_coords = normalize_coordinates(rotated_cross, img_width, img_height)
createLabel('circle', normalized_coords, 'labels/test4')
cv2.imwrite('images/test4.jpg', img)
cv2.imshow("Centered Circle", img)
cv2.waitKey(0)


img_width, img_height = 800, 600
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

# Quarter circle
quarter_circle_radius = min(img_width, img_height) // 4
quarter_circle_points = generate_centered_quarter_circle(quarter_circle_radius, 50, img_width, img_height)
centered_quarter_circle = quarter_circle_points
rotated_cross = rotate_shape(centered_quarter_circle, (img_width/2,img_height/2), 10)
rotated_cross = shift_shape(rotated_cross, 20, -20, img_width, img_height)
draw_shape(img, rotated_cross, (0, 0, 255))
normalized_coords = normalize_coordinates(rotated_cross, img_width, img_height)
createLabel('quartercircle', normalized_coords, 'labels/test4')
cv2.imwrite('images/test4.jpg', img)
cv2.imshow("Centered Quarter Circle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()





# Semi-Circle
img_width, img_height = 800, 600
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)


semicircle_radius = min(img_width, img_height) // 4
semicircle_points = generate_centered_semi_circle(semicircle_radius, 50, img_width, img_height)

# Since the geometric center is at (0, 0), translate the semicircle to the image center
centered_semicircle = semicircle_points

rotated_cross = rotate_shape(centered_semicircle, (img_width/2,img_height/2), 45)
rotated_cross = shift_shape(rotated_cross, -100, 200, img_width, img_height)
fill_shape(img, rotated_cross, (0, 0, 255))
normalized_coords = normalize_coordinates(rotated_cross, img_width, img_height)
createLabel('semicircle', normalized_coords, 'labels/test5')
cv2.imwrite('images/test5.jpg', img)
cv2.imshow("Centered Semicircle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Triangle
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)
triangle_points = generate_centered_triangle(200, img_width, img_height)
centered_triangle = triangle_points
rotated_cross = rotate_shape(centered_triangle, (img_width/2,img_height/2), 45)
rotated_cross = shift_shape(rotated_cross, -100, 400, img_width, img_height)
draw_shape(img, rotated_cross, (0, 0, 255))
normalized_coords = normalize_coordinates(rotated_cross, img_width, img_height)
createLabel('triangle', normalized_coords, 'labels/test6')
cv2.imwrite('images/test6.jpg', img)
cv2.imshow("Centered Triangle", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Pentagon
img_width, img_height = 800, 600
img = np.zeros((img_height, img_width, 3), dtype=np.uint8)

pentagon_radius = min(img_width, img_height) // 4
pentagon_points = generate_centered_pentagon(pentagon_radius, img_width, img_height)
centered_pentagon = pentagon_points
rotated_cross = rotate_shape(centered_pentagon, (img_width/2,img_height/2), 45)
rotated_cross = shift_shape(rotated_cross, 0, -100, img_width, img_height)
draw_shape(img, rotated_cross, (0, 0, 255))
normalized_coords = normalize_coordinates(rotated_cross, img_width, img_height)
createLabel('pentagon', normalized_coords, 'labels/test7')
cv2.imwrite('images/test7.jpg', img)
cv2.imshow("Centered Pentagon", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

