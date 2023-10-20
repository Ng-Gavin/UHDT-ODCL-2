import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def convert1(rgbdata: list):
    rgb = [float(n) for n in rgbdata]

    for i in range(len(rgb)):
        if rgb[i] <= 109:
            rgb[i] = 0
        elif rgb[i] >= 136:
            rgb[i] = 255
        elif rgb[i] < 135 or rgb[i] > 110:
            rgb[i] = 128

    return rgb


def color(rgb: list):
    if rgb == [255, 0, 0]:
        return "RED"
    if rgb == [255, 128, 0]:
        return "ORANGE"
    if rgb == [255, 255, 0]:
        return "YELLOW"
    if rgb == [0, 255, 0]:
        return "GREEN"
    if rgb == [0, 0, 255]:
        return "BLUE"
    if rgb == [128, 0, 128]:
        return "PURPLE"
    if rgb == [0, 0, 0]:
        return "BLACK"
    if rgb == [255, 255, 255]:
        return "WHITE"
    if rgb == [128, 128, 128]:
        return "GRAY"
    if rgb == [150, 75, 0]:
        return "BROWN"

    return "UNKNOWN"


def color_rec(source):
    # cv2 route of opening images
    # image = cv2.imread(source)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # img = image.reshape((-1,3))

    # Pillow route of opening images
    # image = Image.open(image)
    image = source.convert('RGB')
    #plt.imshow(image)
    #plt.show()
    image = np.array(image)
    img = image.reshape((-1, 3))

    # Unit conversion
    img = np.float32(img)

    # kmeans settings
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    retval, labels, centroid = cv2.kmeans(img, 10, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # apply kmeans color rounding to original image
    centers = np.uint8(centroid)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape((image.shape))
    plt.imshow(segmented_image)
    plt.show()
    # mask orignal image to isolate alphanumeric
    mask = cv2.inRange(segmented_image, centers[2], centers[2])
    result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)
    plt.imshow(result)
    plt.show()
    # convert RGB values to color names
    colors = []
    rgb = []
    for i in range(len(centroid)):
        rgb_vals = convert1(centroid[i])
        rgb.append(rgb_vals)
        color_name = color(rgb_vals)
        colors.append(color_name)

    labels = list(labels)
    percent = []

    for i in range(len(centroid)):
        j = labels.count(i)
        j = j / (len(labels))
        percent.append(j)

    # plot the pie chart
    # plt.pie(percent, colors=np.array(centroid/255), labels=colors)
    # plt.show()

    # Sort percent of colors in image from least to greatest
    sorted_arrays = zip(percent, colors, rgb)
    sorted_arrays = sorted(sorted_arrays, key=lambda x: x[0])
    percent, colors, rgb = zip(*sorted_arrays)

    return colors[0], colors[2], rgb[0], rgb[2], colors[1], rgb[
        1], result  # alphanum_string, shape_string, alphanum_rgb, shape_rgb
#f = open('demo.txt', "w")
#f.write(str(color_rec(Image.open('DSC01289-1.jpg'))))
#f.close()
# Testing code
alphanum_string, shape_string, alphanum_rgb, shape_rgb, third_string, third_rgb, result = color_rec(Image.open('./Cropped Targets/image1-0.jpg'))
print(alphanum_string, shape_string, alphanum_rgb, shape_rgb, third_string, third_rgb)