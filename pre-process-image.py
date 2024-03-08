import cv2
import numpy as np
import matplotlib.pyplot as plt
from rembg import remove, new_session
import os
from PIL import Image, ImageEnhance
import torch
from PIL import Image
from RealESRGAN import RealESRGAN


img_path = '../Training Data/Select Cropped/image12cropped0.jpg'
# Device CPU
device = torch.device('cpu')

# Load model and scale factor
model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x4.pth', download=True)

def convert_hsv_to_bgr(img):
    return cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

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

#cv2.imshow('test', im)
# Display the result
#cv2.imshow('Centered Image', img_hsv)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
def gaussian_filter(kernel_size,img,sigma=1, muu=0):
    x, y = np.meshgrid(np.linspace(-1, 1, kernel_size),
                       np.linspace(-1, 1, kernel_size))
    dst = np.sqrt(x**2+y**2)
    normal = 1/(((2*np.pi)**0.5)*sigma)
    gauss = np.exp(-((dst-muu)**2 / (2.0 * sigma**2))) * normal
    gauss = np.pad(gauss, [(0, img.shape[0] - gauss.shape[0]), (0, img.shape[1] - gauss.shape[1])], 'constant')
    return gauss

def fft_deblur(img,kernel_size,kernel_sigma=5,factor='wiener',const=0.002):
    gauss = gaussian_filter(kernel_size,img,kernel_sigma)
    img_fft = np.fft.fft2(img)
    gauss_fft = np.fft.fft2(gauss)
    weiner_factor = 1 / (1+(const/np.abs(gauss_fft)**2))
    if factor!='wiener':
        weiner_factor = factor
    recon = img_fft/gauss_fft
    recon*=weiner_factor
    recon = np.abs(np.fft.ifft2(recon))
    return recon

def removeBackground(img):
    model_name = "unet"
    session = new_session(model_name)
    removed_background = remove(img)
    return removed_background
    #cv2.imshow('test', removed_background)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def edge_detection(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    im = cv2.filter2D(img, -1, kernel)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    return edges
    #cv2.imshow('hello', im)
    #cv2.imshow('test', edges)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

def preprocessing(img):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    im = cv2.filter2D(img, -1, kernel)

def enhancements(img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l2 = clahe.apply(l)
    lab = cv2.merge((l2, a, b))
    contrast_enhanced = cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2HSV)
    return contrast_enhanced



def extract_clusters(img, k):
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

    # Define criteria and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
    retval, labels, centers = cv2.kmeans(pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    # Convert back to 8-bit values
    centers = np.uint8(centers)
    segmented_data = centers[labels.flatten()]
    segmented_image = segmented_data.reshape(img.shape)

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
        print(f"Label: {label}, Color: {color_name} ({hsv}), Count: {count}, Percentage: {percentage:.2f}")
        if color_count[color_name] > 0 or color_name == 'BACKGROUND':
            continue
        else:
            colors.append((color_name, label, hsv, percentage))
            color_count[color_name] += 1
    return segmented_image, colors[0][0], colors[1][0], colors[0][2], colors[1][2]



def denoise_image(img):
    return cv2.fastNlMeansDenoisingColored(img, None, h=10, templateWindowSize=7, searchWindowSize=21)




def goThroughFolder(folder_path):
    images = os.listdir(folder_path)
    for image in images:
        full_path = os.path.join(folder_path, image)
        if os.path.isfile(full_path):
            if full_path.lower().endswith(('.jpg', '.jpeg', 'png')):
                img = cv2.cvtColor(cv2.imread(full_path), cv2.COLOR_BGR2HSV)
                #enhanced_img = cv2.addWeighted(img, 10, np.zeros(img.shape, img.dtype), 0, 0)
                #width = img.shape[0]
                #height = img.shape[1]
                #pillow_img = Image.open(full_path).convert('RGB')
                #upscaled_img = model.predict(pillow_img)
                #upscaled_img_cv = cv2.cvtColor(np.array(upscaled_img), cv2.COLOR_RGB2BGR)
                #resized_img = cv2.resize(upscaled_img_cv, (width, height), interpolation=cv2.INTER_AREA)
                denoised_image = denoise_image(img)
                segmented_image = extract_clusters(denoised_image, 10)[0]
                segmented_image = denoise_image(segmented_image)
                #gray = cv2.cvtColor(denoised_image, cv2.COLOR_BGR2GRAY)
                #blurred = cv2.GaussianBlur(gray, (7, 7), 0)
                #thresh = cv2.adaptiveThreshold(blur, 255,00
                #                               cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
                cv2.imshow('Upscale Test', convert_hsv_to_bgr(segmented_image))
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                #denoised_image = cv2.fastNlMeansDenoisingColored(img, None, h=1, templateWindowSize=7,
                #                                                 searchWindowSize=21)
                #segmented_image = extract_clusters(denoised_image, 10)[0]
                #segmented_image2 = extract_clusters(segmented_image, 10)[0]
                #edges = edge_detection(segmented_image)
                #cv2.imshow('edges', cv2.cvtColor(np.array(upscaled_img), cv2.COLOR_RGB2BGR))
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                #print('hello')
                # original_img = cv2.imread(full_pa0th)
                #gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
                #cv2.imshow('mbruh', gray00)
                #thresh = cv2.adaptiveThreshold(gray, 255
                #                               cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)
                #cv2.imshow("Thresh", thresh)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows(

goThroughFolder('../Training Data/Select Cropped')


