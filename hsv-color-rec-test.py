import cv2
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from rembg import remove
import xattr
import plistlib
import os
from hsv import color_rec





def get_file_comment(file_path):
    # Define the name of the attribute
    attr_name = "com.apple.metadata:kMDItemComment"

    # Read the extended attribute from the file
    try:
        attr_data = xattr.getxattr(file_path, attr_name)
    except:
        return file_path

    # The comment is stored in binary plist format, so we need to deserialize it
    # 'plistlib.loads' expects a bytes object and returns the deserialized plist
    comment = plistlib.loads(attr_data)

    # If the comment exists, it should be a string inside a list
    if comment:
        return comment  # Returning the comment string
    else:
        return None

#print(color_rec('../Training Data/Real Life Cropped Targerts/image2-0.jpg'))

#print(get_file_comment('../Training Data/Real Life Cropped Targets/image2-0.jpg'))

def color_rec_test(directory_path):
    # List all files and directories in the specified path
    images = os.listdir(directory_path)
    exact_match = 0
    order_switched = 0
    at_least_one = 0
    progress = 0
    color_counts = {
        'BLACK': {
            'expected': 0,
            'detected': 0
        },
        'WHITE': {
            'expected': 0,
            'detected': 0
        },
        'RED': {
            'expected': 0,
            'detected': 0
        },
        'ORANGE': {
            'expected': 0,
            'detected': 0
        },
        'BROWN': {
            'expected': 0,
            'detected': 0
        },
        'GREEN': {
            'expected': 0,
            'detected': 0
        },
        'BLUE': {
            'expected': 0,
            'detected': 0
        },
        'PURPLE': {
            'expected': 0,
            'detected': 0
        }
    }
    for image in images:
        bg_color = ""
        alphanum_color = ""
        # Create the full path to the entry
        full_path = os.path.join(directory_path, image)
        if os.path.isfile(full_path):
            if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                try:
                    bg_color, alphanum_color = get_file_comment(full_path).split(' ')
                except:
                    print(get_file_comment(full_path))
                try:
                    color_counts[bg_color]['expected'] += 1
                    color_counts[alphanum_color]['expected'] += 1
                except:
                    print(full_path)
            else:
                continue
        try:
            detected_bg_color, detected_alphanum_color, bg_hsv, alphanum_hsv = color_rec(full_path)
        except:
            print(color_rec(full_path))
            print(color_rec(full_path)[0], color_rec(full_path)[1], color_rec(full_path)[2],color_rec(full_path)[3],)
            print(full_path + " is causing an error?")
        color_counts[detected_bg_color]['detected'] += 1
        color_counts[detected_alphanum_color]['detected'] += 1
        progress += 1
        if detected_bg_color == bg_color or  detected_bg_color == alphanum_color or detected_alphanum_color == alphanum_color or detected_alphanum_color == bg_color:
            if detected_bg_color == bg_color and detected_alphanum_color == alphanum_color:
                exact_match += 1
                order_switched += 1
                at_least_one += 1
            elif detected_bg_color == alphanum_color and detected_alphanum_color == bg_color:
                order_switched += 1
                at_least_one += 1
                print(
                    f'N: {progress}) Path: {full_path}, Detected BG: {detected_bg_color} ({bg_hsv}), Expected BG: {bg_color}, Detected Alphanum: {detected_alphanum_color} ({alphanum_hsv}), Expected Alphanum: {alphanum_color} ::SWITCHED::')
            elif detected_bg_color == bg_color or detected_alphanum_color == alphanum_color:
                print(
                    f'N: {progress}) Path: {full_path}, Detected BG: {detected_bg_color} ({bg_hsv}), Expected BG: {bg_color}, Detected Alphanum: {detected_alphanum_color} ({alphanum_hsv}), Expected Alphanum: {alphanum_color} ::ATLEAST1::')
                at_least_one += 1
            else:
                print(
                    f'N: {progress}) Path: {full_path}, Detected BG: {detected_bg_color} ({bg_hsv}), Expected BG: {bg_color}, Detected Alphanum: {detected_alphanum_color} ({alphanum_hsv}), Expected Alphanum: {alphanum_color}')
        else:
            print(f'Path: {full_path}, Detected BG: {detected_bg_color} ({bg_hsv}), Expected BG: {bg_color}, Detected Alphanum: {detected_alphanum_color} ({alphanum_hsv}), Expected Alphanum: {alphanum_color}')
    print('RESULTS')
    print(f'N: {len(images)}, Exact Matches: {exact_match}, Exact Matches and Switched Order: {order_switched}, At Least One: {at_least_one}')
    black, white, red, orange, brown, green, blue, purple = color_counts
    for key in color_counts.keys():
        print(f'EXPECTED {key}: {color_counts[key]["expected"]}  DETECTED {key}: {color_counts[key]["detected"]} ({color_counts[key]["detected"]/color_counts[key]["expected"] * 100 if color_counts[key]["expected"] > 0 else "Detected " + str(color_counts[key]["detected"]) + "when none were detected"})')



# Specify the path to your directory
path_to_directory = "../Training Data/Combination Set"
color_rec_test(path_to_directory)
