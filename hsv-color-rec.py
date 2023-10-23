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
        if v > 240:
            return "WHITE"
    if v < 20:
        return "BLACK"

    if h > 156.625 or h <= 11.1875:
        # if v < 155:
        #    return 'BROWN'
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
    elif 11.1875 < h <= 28:
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
        if s < 70:
            return 'PURPLE'
        else:
            return "BLUE"
    elif 122 < h <= 156.625:
        if s < 23:
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
    k = 10
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
    plt.imshow(segmented_image_in_rgb)
    plt.show()
    if colors[0][0] == "ORANGE":
        lowerbound1 = np.array([11, 0, 198])
        upperbound1 = np.array([28, 255, 255])
        mask1 = cv2.inRange(segmented_image, lowerbound1, upperbound1)
        mask = mask1
        result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)
        cv2.imshow('mask1', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if colors[1][0] == "BROWN":
        lowerbound1 = np.array([0, 0, 102])
        upperbound1 = np.array([11, 255, 255])
        lowerbound2 = np.array([11, 0, 0])
        upperbound2 = np.array([28, 255, 198])
        lowerbound3 = np.array([156, 0, 102])
        upperbound3 = np.array([181, 255, 255])
        mask1 = cv2.inRange(segmented_image, lowerbound1, upperbound1)
        mask2 = cv2.inRange(segmented_image, lowerbound2, upperbound2)
        mask3 = cv2.inRange(segmented_image, lowerbound3, upperbound3)
        lowerbound4 = np.array([11, 0, 198])
        upperbound4 = np.array([28, 255, 255])
        mask4 = cv2.inRange(segmented_image, lowerbound4, upperbound4)
        mask = mask1 + mask2 + mask3
        result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)
        cv2.imshow('mask1', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    """
    plt.imshow(segmented_image_in_rgb)
    plt.show()
    lowerbound1 = np.array([0, 0, 102])
    upperbound1 = np.array([11, 255, 255])
    lowerbound2 = np.array([11, 0, 0])
    upperbound2 = np.array([28, 255, 198])
    lowerbound3 = np.array([156, 0, 102])
    upperbound3 = np.array([181, 255, 255])
    mask1 = cv2.inRange(segmented_image, lowerbound1, upperbound1)
    mask2 = cv2.inRange(segmented_image, lowerbound2, upperbound2)
    mask3 = cv2.inRange(segmented_image, lowerbound3, upperbound3)
    lowerbound4 = np.array([11, 0, 198])
    upperbound4 = np.array([28, 255, 255])
    mask4 = cv2.inRange(segmented_image, lowerbound4, upperbound4)
    mask = mask1+mask2+mask3
    result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask)
    cv2.imshow('mask1', mask)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    # print(colors[0][0])
    # mask1 = cv2.inRange(img_hsv, np.array([119, 29, 222]), np.array([119, 29, 222]))
    # result1 = cv2.bitwise_and(original_img, original_img, mask=mask1)
    # plt.imshow(cv2.cvtColor(result1, cv2.COLOR_HSV2RGB))
    # plt.show()
    # print(colors[1][0])
    # mask2 = cv2.inRange(segmented_image, centers[colors[1][1]], centers[colors[1][1]])
    # result2 = cv2.bitwise_and(original_img, original_img, mask=mask2)
    # plt.imshow(cv2.cvtColor(result2, cv2.COLOR_HSV2RGB))
    # plt.show()
    # plt.imshow(result1 +result2)
    # plt.show()
    # #print(colors[0][0])
    # mask1 = cv2.inRange(segmented_image, centers[colors[0][1]], centers[colors[0][1]])
    # result1 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask1)
    # #plt.imshow(cv2.cvtColor(result1, cv2.COLOR_HSV2RGB))
    # cv2.imshow('mask1', mask1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('mask1', result1)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(colors[1][0])
    # mask2 = cv2.inRange(segmented_image, centers[colors[1][1]], centers[colors[1][1]])
    # result2 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask2)
    # cv2.imshow('mask2', mask2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('mask1', result2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imshow('mask1', result1+result2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    #plt.imshow(cv2.cvtColor(result2, cv2.COLOR_HSV2RGB))
    #plt.show()
    #plt.imshow(result1 +result2)
    #plt.show()
    return colors[0][0], colors[1][0], colors[0][2], colors[1][2]

print(color_rec('../Training Data/Combination Set/125-image23-24.jpg'))
