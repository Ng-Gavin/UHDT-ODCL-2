import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

def identify_color(cluster_center):
    # Determine ranges
    # CV2: H: 0-179, S: 0-255, V: 0-255
    # Normal Def: H: 0-1, 0-1
    # H scale factor: 0.49722222222222222 (360->179)
    # S and V scale factor: 255 (1 -> 255)

    h, s, v = cluster_center

    if s < 30:
        if v < 50:
            return "Black"
        elif v > 200:
            return "White"
        else:
            return "Gray"
    if v < 50:
        return "Black"

    if 0 <= h <= 11.1875:
        return "Red"
    elif 11.1875 < h <= 29.83333333:
        if True:
            return "Orange" #30 degrees
        else:
            return "Brown"
    elif 29.83333333 < h <= 78.3125:
        return "Green"
    elif 78.3125 < h <= 119.33333333:
        return "Blue"
    elif 119.33333333 < h <= 179:
        return "Purple"

    return "Unknown"



# Read the image
# Target 7 brown and orange test
#image_path = './Target Printouts/Target11.jpg'
image_path = './Cropped Targets/real3-1.jpg'


img = cv2.imread(image_path)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
"""
plt.imshow(img)
plt.show()

print(img_hsv.shape)
cv2.imshow('bruh', img_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


# Reshape the image to a 2D array of pixels
pixels = img_hsv.reshape((-1, 3))
pixels = np.float32(pixels)

# Define criteria and apply kmeans()
criteria = (cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
k = 8
retval, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Convert back to 8-bit values
centers = np.uint8(centers)
segmented_data = centers[labels.flatten()]
segmented_image = segmented_data.reshape(img.shape)
segmented_image_in_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_HSV2RGB)
#print('Test', segmented_image[1056][2651])
#f = open('mbruh.txt', 'w')
#f.write(str(segmented_image))
#f.close()
#Image.fromarray(segmented_image_in_rgb, 'RGB').show()
plt.imshow(segmented_image_in_rgb)
plt.show()
# Count occurrences of each cluster label
unique_labels, counts = np.unique(labels, return_counts=True)

# Calculate total number of pixels
total_pixels = pixels.shape[0]

# Identify and count the colors, and calculate their percentages
color_data = []
for label, count in zip(unique_labels, counts):
    color_name = identify_color(centers[label])
    print(label, ':', centers[label])
    percentage = (count / total_pixels) * 100
    color_data.append((color_name, count, percentage, label))

# Sort by percentage in descending order
color_data.sort(key=lambda x: x[2], reverse=True)

# Print the sorted data
for color_name, count, percentage, label in color_data:
    print(f"Label: {label}, Color: {color_name}, Count: {count}, Percentage: {percentage:.2f}")
