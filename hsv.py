import cv2
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from rembg import remove

def identify_color(cluster_center):
    # Determine ranges
    # CV2: H: 0-179, S: 0-255, V: 0-255
    # Normal Def: H: 0-1, 0-1
    # H scale factor: 0.49722222222222222 (360->179)
    # S and V scale factor: 255 (1 -> 255)

    h, s, v = cluster_center

    if s < 30:
        if v < 50:
            return "BLACK"
        if v > 250:
            return "WHITE"
    if v < 20:
        return "BLACK"

    if h > 156.625 or h <= 10:
        # if v < 155:
        #    return 'BROWN'
        if (h > 180 and (h-180) < -3) or h > 3:

            if 3 < h < 8:
                if s < 149:
                    return "BROWN"
                else:
                    return "RED"

            if s <= 105:
                if s < 65:
                    return 'BROWN'
                else:
                    if v < 165:
                        return 'BROWN'
                    else:
                        return 'RED'
            else:
                return "RED"
        elif h < 3 or (h-180) > -3:
            if s < 200:
                return "BROWN"
            else:
                return "RED"
            return "RED"
        else:
            return 'RED'
    elif 10 < h <= 28:
        if v < 135:
            if s < 90:
                return "BROWN"  # 30 degrees
            else:
                return "ORANGE"
        else:
            return "ORANGE"
    elif 28 < h <= 93:
        if 28.5 < h < 33:
            return 'BACKGROUND'
        else:
            return "GREEN"
    elif 93 < h <= 122:
        if h < 110:
            return "BLUE"
        else:
            if s < 70:
                return 'PURPLE'
            else:
                return "BLUE"
    elif 122 < h <= 156.625:
        if s < 20:
            return "BROWN"
        return "PURPLE"
    else:
        return "Unknown"

def color_rec (image_path):
    color_count = {
        'BLACK': 0,
        'WHITE': 0,
        'RED': 0,
        'BROWN': 0,
        'ORANGE': 0,
        'GREEN': 0,
        'BLUE': 0,
        'PURPLE': 0,
        'BACKGROUND': 0,
    }

    # Read images in CV2:
    img = Image.open(image_path)

    # Remove background and replace with yellow:
    img = remove(img)
    bg_image = Image.new("RGBA", img.size, (255, 251, 0))
    img = Image.alpha_composite(bg_image, img.convert('RGBA'))

    # Convert the image to
    img_hsv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV)

    # Reshape the image to a 2D array of pixels
    pixels = img_hsv.reshape((-1, 3))
    pixels = np.float32(pixels)

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    k = 8
    retval, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit values
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img_hsv.shape)

    # Count occurrences of each cluster label
    unique_labels, counts = np.unique(labels, return_counts=True)

    # Calculate total number of pixels
    total_pixels = pixels.shape[0]

    # Identify and count the colors, and calculate their percentages
    color_data = []

    for label, count in zip(unique_labels, counts):
        color_name = identify_color(centers[label])
        percentage = (count / total_pixels) * 100
        hsv = np.array(centers[label]).tolist()
        color_data.append((color_name, count, percentage, label, hsv))

    # Sort by percentage in descending order
    color_data.sort(key=lambda x: x[2], reverse=True)

    # Unique colors identified
    colors = []

    # Print the sorted data
    for color_name, count, percentage, label, hsv in color_data:
        #print(f"Label: {label}, Color: {color_name}, Count: {count}, Percentage: {percentage:.2f}")
        if color_count[color_name] > 0 or color_name == 'BACKGROUND':
            continue
        else:
            colors.append((color_name, label, hsv, percentage))
            color_count[color_name] += 1
    try:
        return colors[0][0], colors[1][0], colors[0][2], colors[1][2]
    except:
        print(image_path)
        print(colors[0][0])
        print(colors[1][0])
        print(colors[0][2])
        print(colors[1][2])