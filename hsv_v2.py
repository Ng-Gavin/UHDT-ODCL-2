import cv2
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from rembg import remove
from masks import create_masks, create_masks_test
from pathlib import Path


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
        if v > 246:
            return "WHITE"
    if v < 20:
        return "BLACK"
    if h > 156.625 or h <= 10:
        if h > 9:
            return 'BROWN'
        else:
            if s < 130:
                if s < 40:
                    return 'BROWN'
                if v < 165:
                    return 'BROWN'
                elif v > 0.9 * 255:
                    if s > 0.45 * 255:
                        return 'RED'
                    else:
                        return 'ORANGE'
                else:
                    return 'RED'
            elif v > 0.9 * 255:
                if s > 0.48 * 255:
                    return 'RED'
                else:
                    return 'ORANGE'
            else:
                if s < 142:
                    return 'BROWN'
                else:
                    return 'RED'

        """
        if s < 160:

        if v < 165:
            return 'BROWN'
        else:
            return 'RED'
        """
        """
        if (h > 180 and (h-180) < -3) or h > 3:
            if 3 < h < 7:
                if s < 149:
                    return "BROWN"
                else:
                    return "RED"
            if (h - 180) > -3:
                if s < 200:
                    return "BROWN"
                else:
                    return "RED"
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
        
    """
    elif 10 < h <= 33:
        if 28.5 < h < 33 and s > 250 and v > 250:
            return 'BACKGROUND'
        if s < 100:
            return 'BROWN'
        if v < 160:
            return "BROWN"
        else:
            return 'ORANGE'
        """
        if h > 25:
            if v < 180:
                return 'BROWN'
            else:
                return "ORANGE"

        if v < 230:
            if s < 230:
                return "BROWN"  # 30 degrees
            else:
                return "ORANGE"
        else:
            return "ORANGE"
    """
    elif 33 < h <= 99:
            return "GREEN"
    elif 99 < h <= 122:
        return "BLUE"
    elif 122 < h <= 156.625:
        if s < 20:
            return "BROWN"
        elif s < 43:
            return 'BLUE'
        else:
            return "PURPLE"
    else:
        return "UNKNOWN"

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
    img_test = ImageEnhance.Contrast(img)
    #img.show()
    # Convert the image to
    img_hsv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV)


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
        #print(label, ':', centers[label])

    # Sort by percentage in descending order
    color_data.sort(key=lambda x: x[2], reverse=True)

    # Unique colors identified
    colors = []

    # Print the sorted data
    for color_name, count, percentage, label, hsv in color_data:
        #print(f"Label: {label}, Color: {color_name} ({hsv}), Count: {count}, Percentage: {percentage:.2f}")
        if color_count[color_name] > 0 or color_name == 'BACKGROUND':
            continue
        else:
            colors.append((color_name, label, hsv, percentage))
            color_count[color_name] += 1
    #cv2.imshow('segmented', segmented_image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    figs, axs = plt.subplots(1, 4)
    figs.suptitle(image_path)
    axs[0].imshow(cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB))
    axs[1].imshow(cv2.cvtColor(segmented_image, cv2.COLOR_HSV2RGB))
    mask1 = create_masks_test(segmented_image, colors[0][0], color_data, 10)
    result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask1)
    axs[2].imshow(cv2.cvtColor(result, cv2.COLOR_HSV2RGB))
    file_name = f'./dummy/{Path(image_path).stem}_mask1{Path(image_path).suffix}'
    #cv2.imwrite(file_name, mask1)
    file_name = f'./dummy/{Path(image_path).stem}_mask1_color{Path(image_path).suffix}'
    #cv2.imwrite(file_name, result)
    #cv2.imshow('mask1', mask1)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    mask2 = create_masks_test(segmented_image, colors[1][0], color_data, 10)
    mask2 = create_masks_test(segmented_image, colors[1][0], color_data, 10)
    result = cv2.bitwise_and(segmented_image, segmented_image, mask=mask2)
    axs[3].imshow(cv2.cvtColor(result, cv2.COLOR_HSV2RGB))
    file_name = f'./dummy/{Path(image_path).stem}_mask2{Path(image_path).suffix}'
    #cv2.imwrite(file_name, mask2)
    file_name = f'./dummy/{Path(image_path).stem}_mask2_color{Path(image_path).suffix}'
    #cv2.imwrite(file_name, result)
    plt.tight_layout()
    #plt.show()
    #cv2.imshow('mask2', result)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return colors[0][0], colors[1][0], colors[0][2], colors[1][2]

print(color_rec('../Training Data/image_Sat Oct 28 22_52_59 copy removed/image19 copy.jpg'))