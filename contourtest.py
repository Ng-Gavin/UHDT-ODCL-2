import os, cv2
import numpy as np
from matplotlib import pyplot as plt

dir = 'colored_eval'
for img_path in os.listdir(dir):
    if (img_path.endswith(('.jpg', '.png'))):
        img = cv2.imread(os.path.join(dir, img_path))
        cv2.imshow('Reg image', img)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        eq_img = cv2.equalizeHist(gray)
        #plt.hist(eq_img.flat, bins=100, range=(0, 255))
        #plt.show()
        clahe = cv2.createCLAHE(clipLimit=1, tileGridSize=(8,8))
        cl_img = clahe.apply(gray)
        _, thresh1 = cv2.threshold(cl_img, 200, 150, cv2.THRESH_BINARY)
        _, thresh2 = cv2.threshold(cl_img, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 1)
        cv2.imshow('Eq image', eq_img)
        cv2.imshow('Clahe', cl_img)
        cv2.imshow('Thresh 1', thresh1)
        cv2.imshow('Thresh 2', thresh2)
        cv2.imshow('Contours', img)
        cv2.waitKey(0)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, 20, 20)

        # Find contours0000000iterm
        #contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image
        # cv2.drawContours(target_image, contours, contour_index, color, thickness)
        # Use contour_index = -1 to draw all contours
        #cv2.drawContours(image, contours, -1, (0, 255, 0), 1)

        # Display the image with contours
        #_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        #thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                               cv2.THRESH_BINARY, 31, 21)
        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # ret3, th3 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        # cv2.imshow('Original Image', image)
        # cv2.imshow('Thresh', th3)0
        # cv2.waitKey(0)

