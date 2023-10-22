import cv2
from PIL import Image, ImageEnhance
import matplotlib.pyplot as plt
import numpy as np
from rembg import remove
# Read images in CV2:
img = Image.open('../Training Data/Real Life Cropped Targerts/image7-3.jpg')

# Remove background and replace with yellow:
img = remove(img)
bg_image = Image.new("RGBA", img.size, (255, 251, 0))
img = Image.alpha_composite(bg_image, img.convert('RGBA'))

# Convert the image to
img_hsv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2HSV)

mask1 = cv2.inRange(segmented_image, centers[0], centers[0])
result1 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask1)
mask2 = cv2.inRange(segmented_image, centers[1], centers[1])
result2 = cv2.bitwise_and(segmented_image, segmented_image, mask=mask2)
plt.imshow(result2)
plt.show()