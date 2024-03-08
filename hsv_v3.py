import cv2
import numpy as np
import torch
from RealESRGAN import RealESRGAN
from rembg import remove, new_session
from PIL import Image
def removeBackground(img):
    model_name = "unet"
    session = new_session(model_name)
    removed_background = remove(img)
    return removed_background
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

def denoise_image(img):
    return cv2.fastNlMeansDenoisingColored(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

def create_masks(image, color, color_data):
    mask = 0
    for color_name, count, percentage, label, hsv in color_data:
        if color_name == color:
            mask += cv2.inRange(image, np.array(hsv), np.array(hsv))
    return mask

def edge_detection(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    im = cv2.filter2D(img, -1, kernel)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges
def segment_image(img, k):
    # Convert image to HSV from RGB

    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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

    # Reshape the image to a 2D array of pixels
    pixels = img.reshape((-1, 3))
    pixels = np.float32(pixels)
    total_pixels = pixels.shape[0]

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    retval, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit values
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img.shape)

    return segmented_image, color_count, centers, labels, total_pixels


def extract_colors(color_count, centers, labels, total_pixels, debug = False):
    unique_labels, counts = np.unique(labels, return_counts=True)

    # Identify and count the colors, and calculate their percentages
    color_data = []

    for label, count in zip(unique_labels, counts):
        color_name = identify_color(centers[label])
        percentage = (count / total_pixels) * 100
        hsv = np.array(centers[label]).tolist()
        color_data.append((color_name, count, percentage, label, hsv))
        if debug:
            print(label, ':', centers[label])

    # Sort by percentage in descending order
    color_data.sort(key=lambda x: x[2], reverse=True)

    # Unique colors identified
    colors = []

    # Print the sorted data
    for color_name, count, percentage, label, hsv in color_data:
        if debug:
            print(f"Label: {label}, Color: {color_name} ({hsv}), Count: {count}, Percentage: {percentage:.2f}")
        if color_count[color_name] > 0 or color_name == 'BACKGROUND':
            continue
        else:
            colors.append((color_name, label, hsv, percentage))
            color_count[color_name] += 1
    return colors, color_data

def upscale_image(img):
    device = torch.device('cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth', download=True)
    width = img.shape[0]
    height = img.shape[1]
    pillow_img = Image.fromarray(img)
    upscaled_img = np.array(model.predict(pillow_img))
    resized_img = cv2.resize(upscaled_img, (width, height), interpolation=cv2.INTER_AREA)
    return resized_img

def upscale_image1(img):
    device = torch.device('cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth', download=True)
    width = img.shape[0]
    height = img.shape[1]
    pillow_img = Image.fromarray(img)
    upscaled_img = np.array(model.predict(pillow_img))
    return upscaled_img

def increase_contrast(img):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    contrast_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
    return contrast_img

def enhance_image(img):
    denoised_img = denoise_image(img)
    upscaled_img = upscale_image(denoised_img)
    denoised_img = denoise_image(increase_contrast(denoise_image(upscaled_img)))
    return denoised_img#upscaled_img

def enhance_image1(img):
    denoised_img = denoise_image(img)
    upscaled_img = upscale_image1(denoised_img)
    denoised_img = denoise_image(increase_contrast(denoise_image(upscaled_img)))
    return denoised_img#upscaled_img
def detect_edges(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred_img = cv2.GaussianBlur(gray_img, (3,3), 0)
    edges = cv2.Canny(blurred_img, 100, 200)
    return edges


def color_rec(img):
    enhanced_img = img
    segmented_img, color_count, centers, labels, total_pixels = segment_image(enhanced_img, 10)
    colors, color_data = extract_colors(color_count, centers, labels, total_pixels, False)
    detected_bg_color= colors[0][0]
    detected_alphanum_color = colors[1][0]
    bg_hsv = colors[0][2]
    alphanum_hsv = colors[1][2]
    bg_mask = create_masks(segmented_img, detected_bg_color, color_data)
    bg_mask_result = cv2.bitwise_and(segmented_img, segmented_img, mask=bg_mask)
    alphanum_mask = create_masks(segmented_img, detected_alphanum_color, color_data)
    alphanum_mask_result = cv2.bitwise_and(segmented_img, segmented_img, mask=alphanum_mask)
    return detected_bg_color, detected_alphanum_color, bg_hsv, alphanum_hsv, bg_mask, alphanum_mask


img = cv2.imread('../Training Data/Select Cropped/image90cropped0.jpg')
cv2.imshow("Mask", cv2.cvtColor(segment_image(img, 10)[0], cv2.COLOR_HSV2BGR))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Mask", color_rec(img)[4])
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow("Mask", color_rec(img)[5])
cv2.waitKey(0)
cv2.destroyAllWindows()
#print('Regular results', color_rec(img)[0:2])
#print('Enhanced image results', color_rec(enhance_image(img))[0:2])
#print('Super resolution 2x', color_rec(upscale_image(upscale_image(img)))[0:2])
#cv2.imshow('Regular Image', img)
#cv2.imshow('Increased Contrast', increase_contrast(img))
#cv2.imshow('Denoised Image', increase_contrast(denoise_image(img)))
#cv2.imshow('Enhanced Image', enhance_image(img))

#cv2.imshow('Segment image', detect_edges(upscale_image(enhance_image(increase_contrast(segment_image(img, 10)[0])))))
#cv2.imshow('Edges for Enhanced Image', detect_edges(enhance_image(increase_contrast(increase_contrast(upscale_image(upscale_image(img)))))))

#cv2.waitKey(0)
#cv2.destroyAllWindows()

#print(color_rec(cv2.cvtColor(cv2.imread('../Training Data/Select Cropped/image75cropped1.jpg'), cv2.COLOR_BGR2HSV)))
#test_mask = color_rec(cv2.cvtColor(cv2.imread('../Training Data/Select Cropped/image8cropped1.jpg'), cv2.COLOR_BGR2HSV))[4]
#test_mask = cv2.cvtColor(segment_image(cv2.imread('../Training Data/Select Cropped/image8cropped1.jpg'), 10)[0], cv2.COLOR_HSV2BGR)
#cv2.imshow('mbruh', test_mask)
#cv2.waitKey(0)
#cv2.destroyAllWindows()




