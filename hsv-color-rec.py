import numpy as np
import cv2
from PIL import Image

def identify_color(cluster_center):
    # Determine ranges
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

    if h >= 0 and h <= 12:
        return "Red"
    elif h > 12 and h <= 35:
        return "Orange"
    elif h > 165 and h <= 320:
        return "Brown"
    elif h > 35 and h <= 85:
        return "Green"
    elif h > 85 and h <= 120:
        return "Blue"
    elif h > 120 and h <= 165:
        return "Purple"

    return "Unknown"



# Read the image
image_path = './Target Printouts/Target4.jpg'
image_path = './Target Printouts/Target4.jpg'


img = cv2.imread(image_path)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


print(img_hsv.shape)
cv2.imshow('bruh', img_hsv)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Reshape the image to a 2D array of pixels
pixels = img_hsv.reshape((-1, 3))
pixels = np.float32(pixels)

# Define criteria and apply kmeans()
criteria = (cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
k = 3
retval, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

# Convert back to 8-bit values
centers = np.uint8(centers)
segmented_data = centers[labels.flatten()]
segmented_image = segmented_data.reshape(img.shape)
print('Test', segmented_image[1056][2651])
#f = open('mbruh.txt', 'w')
#f.write(str(segmented_image))
#f.close()
Image.fromarray(segmented_image, 'HSV').show()

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
