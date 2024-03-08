from label_maker import read_exif
import os
from hsv_v3 import color_rec
import cv2
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
        },
        'UNKNOWN': {
            'expected': 0,
            'detected': 0
        }
    }
    num_images = 0
    for image in images:
        bg_color = ""
        alphanum_color = ""
        # Create the full path to the entry
        full_path = os.path.join(directory_path, image)
        if os.path.isfile(full_path):
            if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                num_images += 1
                bg_color, alphanum_color = read_exif(full_path)
                color_counts[bg_color]['expected'] += 1
                color_counts[alphanum_color]['expected'] += 1
            else:
                continue
        try:
            #detected_bg_color, detected_alphanum_color, bg_hsv, alphanum_hsv, bg_mask, alphanum_mask = color_rec(full_path)
            detected_bg_color, detected_alphanum_color, bg_hsv, alphanum_hsv, bg_mask, alphanum_mask = color_rec(cv2.imread(full_path))
        except:
            print(full_path + " is causing an error?")
        color_counts[detected_bg_color]['detected'] += 1
        color_counts[detected_alphanum_color]['detected'] += 1
        progress += 1
        if detected_bg_color == bg_color or  detected_bg_color == alphanum_color or detected_alphanum_color == alphanum_color or detected_alphanum_color == bg_color:
            if detected_bg_color == bg_color and detected_alphanum_color == alphanum_color:
                exact_match += 1
                order_switched += 1
                at_least_one += 1
                print(
                    f'N: {progress}) Path: {full_path}, Detected BG: {detected_bg_color} ({bg_hsv}), Expected BG: {bg_color}, Detected Alphanum: {detected_alphanum_color} ({alphanum_hsv}), Expected Alphanum: {alphanum_color} ::EXACT::')
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
            print(f'N: {progress}) Path: {full_path}, Detected BG: {detected_bg_color} ({bg_hsv}), Expected BG: {bg_color}, Detected Alphanum: {detected_alphanum_color} ({alphanum_hsv}), Expected Alphanum: {alphanum_color}')
    print('RESULTS')
    print(f'N: {num_images}, Exact Matches: {exact_match}, Exact Matches and Switched Order: {order_switched}, At Least One: {at_least_one}')
    black, white, red, orange, brown, green, blue, purple, unknown = color_counts
    for key in color_counts.keys():
        print(f'EXPECTED {key}: {color_counts[key]["expected"]}  DETECTED {key}: {color_counts[key]["detected"]} ({color_counts[key]["detected"]/color_counts[key]["expected"] * 100 if color_counts[key]["expected"] > 0 else "Detected " + str(color_counts[key]["detected"]) + " when none were expected"})')



# Specify the path to your directory
path_to_directory = "../Training Data/Select Cropped"
color_rec_test(path_to_directory)
