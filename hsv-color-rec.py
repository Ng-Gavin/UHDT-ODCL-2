import cv2
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from rembg import remove
from hsv import identify_color
from masks import create_masks

def get_limits(color):
    hue = color[0]  # Get the hue value

    # Handle red hue wrap-around
    if hue >= 165:  # Upper limit for divided red hue
        lowerLimit = np.array([hue - 20, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Lower limit for divided red hue
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 20, 255, 255], dtype=np.uint8)
    else:
        lowerLimit = np.array([hue - 20, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 20, 255, 255], dtype=np.uint8)

    return lowerLimit, upperLimit
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

    """
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()
    """
    """
    print(img_hsv.shape)
    cv2.imshow('bruh', img_hsv)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """


    # Reshape the image to a 2D array of pixels
    pixels = img_hsv.reshape((-1, 3))
    pixels = np.float32(pixels)

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    k = 6
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
        print(label, ':', centers[label])

    # Sort by percentage in descending order
    color_data.sort(key=lambda x: x[2], reverse=True)

    # Unique colors identified
    colors = []

    # Print the sorted data
    for color_name, count, percentage, label, hsv in color_data:
        print(f"Label: {label}, Color: {color_name}, Count: {count}, Percentage: {percentage:.2f}")
        if color_count[color_name] > 0 or color_name == 'BACKGROUND':
            continue
        else:
            colors.append((color_name, label, hsv, percentage))
            color_count[color_name] += 1
    #cv2.imshow('segmented', segmented_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    segmented_image_in_rgb = cv2.cvtColor(segmented_image, cv2.COLOR_HSV2RGB)
    original_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    mask1 = create_masks(segmented_image, colors[0][0], color_data)
    result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask1)
    cv2.imshow('mask1', mask1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    mask2 = create_masks(segmented_image, colors[1][0], color_data)
    result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask2)
    cv2.imshow('mask1', mask2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return colors[0][0], colors[1][0], colors[0][2], colors[1][2]

print(color_rec('../Training Data/Last Year Full Compiled/18-image17.jpg'))
