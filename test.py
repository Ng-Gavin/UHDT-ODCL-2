import plistlib

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


print(get_file_comment('../Training Data/Last Year Full Crop/249-image5-64.jpg'))