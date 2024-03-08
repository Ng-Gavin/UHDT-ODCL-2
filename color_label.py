import cv2
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from rembg import remove
import xattr
import plistlib
import os
from hsv_v3 import color_rec
from osxmetadata import *
import subprocess





#print(color_rec('../Training Data/Real Life Cropped Targerts/image2-0.jpg'))

#print(get_file_comment('../Training Data/Real Life Cropped Targets/image2-0.jpg'))
def remove_from_quarantine(file_path):
    subprocess.run(["xattr", "-d", "com.apple.quarantine", file_path])
def get_file_default_app(file_path):
    # Define the name of the attribute
    attr_name = "com.apple.LaunchServices.OpenWith"

    # Read the extended attribute from the file
    try:
        attr_data = xattr.getxattr(file_path, attr_name)
    except:
        return file_path

    # The comment is stored in binary plist format, so we need to deserialize it
    # 'plistlib.loads' expects a bytes object and returns the deserialized plist
    comment = plistlib.loads(attr_data)

    # If the comment exists, it should be a string inside a list
    if attr_data:
        return attr_data  # Returning the comment string
    else:
        return None
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
def color_rec_test(directory_path):
    # List all files and directories in the specified path
    images = os.listdir(directory_path)
    for image in images:
        bg_color = ""
        alphanum_color = ""
        # Create the full path to the entry
        full_path = os.path.join(directory_path, image)
        if os.path.isfile(full_path):
            if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                attr_name = "kMDItemComment"
                try:
                    img = cv2.imread(full_path)
                    detected_bg_color, detected_alphanum_color, bg_hsv, alphanum_hsv, bg_mask, alphanum_mask = color_rec(img)
                    values = f'{detected_bg_color} {detected_alphanum_color}'
                    md = OSXMetaData(full_path)
                    md.set(attr_name, values)
                    default_app = b'bplist00\xd3\x01\x02\x03\x04\x05\x06WversionTpath_\x10\x10bundleidentifier\x10\x00_\x10\x19/Applications/Metamer.app_\x10\x18co.eclecticlight.Metamer\x08\x0f\x17\x1c/1M\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00h'
                    remove_from_quarantine(full_path)
                    xattr.setxattr(full_path, "com.apple.LaunchServices.OpenWith", default_app)
                    print(get_file_comment(full_path))
                except:
                    print(full_path)



# Specify the path to your directory
path_to_directory = "../Training Data/Select Cropped"
color_rec_test(path_to_directory)

