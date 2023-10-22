import cv2
from sklearn.cluster import KMeans
import numpy as np
from PIL import Image, ImageEnhance
import colorsys
import matplotlib.pyplot as plt


def round_rgb_to_color(rgb):
    h, s, v = cluster_center

    if s < 30:
        if v < 50:
            return "BLACK"
        if v > 240:
            return "WHITE"
    if v < 20:
        return "BLACK"

    if h > 156.625 or h <= 11.1875:
        # if v < 155:
        #    return 'BROWN'
        if s <= 90:
            return 'BROWN'
        else:
            return "RED"
    elif 11.1875 < h <= 28:
        if v < 155:
            return "BROWN"  # 30 degrees
        else:
            return "ORANGE"
    elif 28 < h <= 93:
        if 28.5 < h < 33:
            return 'BACKGROUND'
        else:
            return "GREEN"
    elif 93 < h <= 127.78611111:
        return "BLUE"
    elif 127.78611111 < h <= 156.625:
        if s < 23:
            return "BROWN"
        return "PURPLE"
    else:
        return "Unknown"


def color_rec_large(source):
    # Pillow route of opening images
    image = Image.open(source).convert('HSV')
    # image = source.convert('RGB')
    image = np.array(image)
    img = image.reshape((-1, 3))

    # Unit conversion
    img = np.float32(img)

    # kmeans settings
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    retval, labels, centroid = cv2.kmeans(img, 6, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # apply kmeans color rounding to original image
    centers = np.uint8(centroid)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape((image.shape))
    seg_img = Image.fromarray(segmented_image, 'HSV')
    #seg_img.show()

    # Get Percentage of Each Color in Image
    labels = list(labels)
    percent = []
    for i in range(len(centroid)):
        j = labels.count(i)
        j = j / (len(labels))
        percent.append(j)

    # Sort percent of colors in image from least to greatest
    sorted_arrays = zip(percent, centers)
    sorted_arrays = sorted(sorted_arrays, key=lambda x: x[0])
    percent, centers = zip(*sorted_arrays)

    # mask orignal image, two results in case colors are swapped
    mask1 = cv2.inRange(segmented_image, centers[0], centers[0])
    result1 = cv2.bitwise_and(np.ones_like(segmented_image) * 255, np.zeros_like(segmented_image), mask=mask1)
    plt.imshow(result1)
    plt.show()
    mask2 = cv2.inRange(segmented_image, centers[1], centers[1])
    result2 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask2)
    plt.imshow(result2)
    plt.show()
    print(f"Center0: {centers[0]}")
    print(f"Center1: {centers[1]}")

    # Convert HSV colors to RGB
    rgb_list = []
    for sublist in centers:
        RGB = colorsys.hsv_to_rgb(sublist[0] / 255, sublist[1] / 255, sublist[2] / 255)
        RGB = tuple(int(x * 255) for x in RGB)
        rgb_list.append(RGB)

    print(f"RGB0: {rgb_list[0]}")
    print(f"RGB1: {rgb_list[1]}")

    # Round Colors to Valid Competition COlors
    alphanumColor = round_rgb_to_color(rgb_list[0])
    shapeColor = round_rgb_to_color(rgb_list[1])

    return alphanumColor, shapeColor, result1, result2


# Testing code
alphanum_string, shape_string, result1, result2 = color_rec_large('../Training Data/Real Life Cropped Targerts/21-image23-60.jpg')
print(f"Alpha:{alphanum_string}, Shape:{shape_string}")
