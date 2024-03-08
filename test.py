from hsv_v2_dummy import color_rec
import os
import xattr
import plistlib
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

directory_path = "../Training Data/Select Cropped"
num_images = 0
images = os.listdir(directory_path)



for image in images:
    full_path = os.path.join(directory_path, image)
    if os.path.isfile(full_path):
        if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
            num_images += 1
            detected_bg_color, detected_alphanum_color, bg_hsv, alphanum_hsv = color_rec(full_path)
            bg_color, alphanum_color = get_file_comment(full_path).split(' ')
            print(f'N: {num_images}, {full_path}, Detected BG Color: {detected_bg_color}, Detected Alphanum: {detected_alphanum_color}')
