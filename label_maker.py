import json
import xattr
import plistlib
from utils import loop_through_images
from exiftool import ExifToolHelper
import exiftool
from hsv_v3 import color_rec


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

def convert_mac_comment_to_exif(file_path):
    bg_color, alphanum_color = get_file_comment(file_path).split(' ')

    # Use ExifTool to write the properties to the image
    with exiftool.ExifTool() as et:
        command = ['Comment=' + f'{bg_color} {alphanum_color}', file_path]
        et.execute(*command)


def read_exif(file_path):
    with ExifToolHelper() as et:
        metadata = et.get_tags(file_path, ['Comment'])[0]
        expected_bg_color, expected_alphanum_color = metadata['File:Comment'].split(' ')
        #print(expected_bg_color, expected_alphanum_color)
        return expected_bg_color, expected_alphanum_color

#loop_through_images('../Training Data/Select Cropped', convert_mac_comment_to_exif)




