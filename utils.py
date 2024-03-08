import os
import cv2
def loop_through_images (directory_path, operation):
    # List all files and directories in the specified path
    images = os.listdir(directory_path)
    for image in images:
        bg_color = ""
        alphanum_color = ""
        # Create the full path to the entry
        full_path = os.path.join(directory_path, image)
        if os.path.isfile(full_path):
            if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                operation(full_path)
    print('Finished loop.')


def loop_through_cv_images (directory_path, operation):
    # List all files and directories in the specified path
    images = os.listdir(directory_path)
    for image in images:
        bg_color = ""
        alphanum_color = ""
        # Create the full path to the entry
        full_path = os.path.join(directory_path, image)
        if os.path.isfile(full_path):
            if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                results = operation(cv2.imread(full_path))
                print(full_path)
                print(results[0], results[1])
    print('Finished loop.')


